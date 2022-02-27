from pydantic import BaseModel, EmailStr
from typing import Optional
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None
    
class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    hashed_password: str
class User(BaseModel):
    id: int
    is_active: Optional[bool] = True
    email: EmailStr
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
class UserInDB(User):
    hashed_password: str

class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: int 
class ArticleCreate(ArticleBase):
    created_on: Optional[str]
class Article(ArticleBase):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProjectBase(BaseModel):
    name: str
    desc: str
    github_url: str 
    author_id: int 
    package_manager: Optional[int]
    package_manager_url: Optional[str]
    changelog: Optional[str]
    version: Optional[float] = 0.0
    related_frameworks: Optional[set]
    related_languages: Optional[set]
class ProjectCreate(ProjectBase):
    created_on :Optional[str]
    last_updated_on: Optional[str]
class Project(BaseModel):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class LanguageBase(BaseModel):
    text: str
    classname: Optional[str] = 'bg-black'
    author_id: int 
class LanguageCreate(LanguageBase):
    pass
class Language(LanguageBase):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class MediaBase(BaseModel):
    text: str
    classname: Optional[str] = 'bg-black'
    author_id: int 
class MediaCreate(MediaBase):
    pass
class Media(MediaBase):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class FrameworkBase(BaseModel):
    text: str
    classname: Optional[str] = 'bg-black'
    author_id: int 
class FrameworkCreate(FrameworkBase):
    main_lanugage: Optional[int]
class Framework(FrameworkBase):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RelationBase(BaseModel):
    parent:int
    parent_type:str
    child:int
    relation_type:str
    current_status: Optional[bool] = True
    author_id: int 
class RelationCreate(RelationBase):
    pass
class Relation(RelationBase):
    id:int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True