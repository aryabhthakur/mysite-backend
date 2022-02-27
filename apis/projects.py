from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud,models
from database import schemas
from .auth import get_current_active_user
router =  APIRouter()
@router.get("/")
async def get_project_list(limit:int,offset:int,author:int = None,session: Session = Depends(get_db)):
    list = []
    if author is not None:
        projects = session.query(models.Projects).filter_by(author_id=author).limit(limit).offset(offset).all()
    else:
        projects = session.query(models.Projects).limit(limit).offset(offset).all()
    for project in projects:
        get_frameworks = session.query(models.Relations).filter_by(parent=project.id,relation_type='framework',parent_type='project').all()
        frameworks = [] 
        for framework in get_frameworks: 
            get_f = await crud.get_framework(_id=framework.child,session=session)
            if get_f is not None:
                frameworks.append({'relation_id':framework.id,'id':get_f.id,'text':get_f.text,'classname':get_f.classname}) 
        get_languages = session.query(models.Relations).filter_by(parent=project.id,relation_type='language',parent_type='project').all()
        languages = [] 
        for lang in get_languages: 
            get_l = await crud.get_language(_id=lang.child,session=session)
            if get_l is not None:
                languages.append({'relation_id':lang.id,'id':get_l.id,'text':get_l.text,'classname':get_l.classname}) 
        list.append({'info':project,'related_frameworks':frameworks,'related_languages':languages})
    return {'limit':limit,'offset':offset,'list':list}

@router.get("/{_id}")
async def get_project(_id:int,session: Session = Depends(get_db)):
    """
    Get Single Project by <b>ID</b> provided in List Projects
    """
    try:
        project = session.query(models.Projects).get(_id)
        get_frameworks = session.query(models.Relations).filter_by(parent=_id,relation_type='framework',parent_type='project').all()
        frameworks = [] 
        for framework in get_frameworks: 
            get_f = await crud.get_framework(_id=framework.child,session=session)
            if get_f is not None:
                frameworks.append({'relation_id':framework.id,'id':get_f.id,'text':get_f.text,'classname':get_f.classname}) 
        get_languages = session.query(models.Relations).filter_by(parent=_id,relation_type='language',parent_type='project').all()
        languages = [] 
        for lang in get_languages: 
            get_l = await crud.get_language(_id=lang.child,session=session)
            if get_l is not None:
                languages.append({'relation_id':lang.id,'id':get_l.id,'text':get_l.text,'classname':get_l.classname}) 
        get_articles = session.query(models.Relations).filter_by(child=_id,relation_type='project',parent_type='article').all()
        articles = []
        for article in get_articles: 
            get_p = await crud.get_article(_id=article.parent,session=session)
            if get_p is not None:
                articles.append({'title':get_p.title}) 
        return {'project':project,'related_frameworks':frameworks,'related_languages':languages,'related_articles':articles}
    except:
        raise HTTPException(500,'Something went wrong')

@router.post("/create")
async def create_project(_project: schemas.ProjectCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        creation_data = []
        related_frameworks =  _project.related_frameworks
        related_languages =  _project.related_languages
        create_project = await crud.create_projects(_project, session)
        for lang in related_languages:
            create_relation = await crud.create_relations({'parent':create_project.id,'parent_type':'project','child':lang,'relation_type':'language','author_id':check_login.id}, session)
            creation_data.append({'related_lang':lang,'relation_id':create_relation.id})
        for framework in related_frameworks:
            create_relation = await crud.create_relations({'parent':create_project.id,'parent_type':'project','child':framework,'relation_type':'framework','author_id':check_login.id}, session)
            creation_data.append({'related_lang':framework,'relation_id':create_relation.id})
        creation_data.append({'created_project':create_project})
        return creation_data
    except:
        raise HTTPException(404,'Something went wrong')

@router.put("/update/{id}")
async def update_projects(id:int,info_update:schemas.ProjectCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)) -> schemas.Project:
    try:
        update = await crud.update_projects(id=id,info_update=info_update,db=session,cuid=check_login.id)
        return update
    except:
        raise HTTPException(404,'Something went wrong')

@router.delete("/delete/{id}")
async def delete_projects(id:int,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        delete = await crud.delete_projects(id=id,db=session,cuid=check_login.id)
        return delete
    except:
        raise HTTPException(404,'Something went wrong')