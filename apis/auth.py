from typing import Optional
from dotenv import dotenv_values
from jose import JWTError, jwt
from database import schemas,models
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database.crud import verify_password,create_user
from database.database import get_db

env = dotenv_values(".env")
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(email:str,password:str,db):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env['SECRET_KEY'], algorithm=env['ALGORITHM'])
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_usr = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cannot Find User based on token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_JWT = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="JWT error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env['SECRET_KEY'], algorithms=env['ALGORITHM'])
        id: str = payload.get("sub") #type: ignore
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception_JWT
    user =  db.query(models.Users).get(token_data.id)
    if user is None:
        raise credentials_exception_usr
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.is_active != True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: schemas.UserCreate,session: Session = Depends(get_db)):
    if env["IS_PLATFORM"] == '0':
        if session.query(models.Users.id).count() >= 1:
            raise HTTPException(200,'Blog Already has Sudo User (IS_PLATFORM=False)')
        else:
            if session.query(models.Users.email).filter_by(email=user.email).first() is None:
                try:
                        create = await create_user(user, session)
                        return create
                except:
                    raise HTTPException(500,'Internal Server Error')
            else:
                raise HTTPException(406,'Email Already exist!')
    else:
        if session.query(models.Users.email).filter_by(email=user.email).first() is None:
            try:
                    create = await create_user(user, session)
                    return create
            except:
                raise HTTPException(500,'Internal Server Error')
        else:
            raise HTTPException(406,'Email Already exist!')

@router.get("/users/me/")
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user))-> schemas.User:
    return current_user
