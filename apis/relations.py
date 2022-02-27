from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud
from database import schemas
from .auth import get_current_active_user
router =  APIRouter()

@router.post("/create")
async def create_project(_relation: schemas.RelationCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        create = await crud.create_relations(_relation, session)
        return create
    except:
        raise HTTPException(404,'Something went wrong')

@router.put("/update/{id}")
async def update_projects(id:int,info_update:schemas.RelationCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)) -> schemas.Project:
    try:
        update = await crud.update_relations(id=id,info_update=info_update,db=session,cuid=check_login.id)
        return update
    except:
        raise HTTPException(404,'Something went wrong')

@router.delete("/delete/{id}")
async def delete_projects(id:int,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        delete = await crud.delete_relations(id=id,db=session,cuid=check_login.id)
        return delete
    except:
        raise HTTPException(404,'Something went wrong')