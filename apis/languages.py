from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud,models
from database import schemas
from .auth import get_current_active_user
router =  APIRouter()
@router.get("/")
async def get_language_list(limit:int,offset:int,author:int = None,session: Session = Depends(get_db)):
    list = []
    if author is not None:
        languages = session.query(models.Languages).filter_by(author_id=author).limit(limit).offset(offset).all()
    else:
        languages = session.query(models.Languages).limit(limit).offset(offset).all()
    for language in languages:
        get_frameworks = session.query(models.Frameworks).filter_by(main_lanugage=language.id).all()
        frameworks = [] 
        for framework in get_frameworks: 
            get_f = await crud.get_framework(_id=framework.id,session=session)
            if get_f is not None:
                frameworks.append({'relation_id':framework.id,'text':get_f.text,'classname':get_f.classname}) 
        get_projects = session.query(models.Relations).filter_by(child=language.id,relation_type='language',parent_type='project').all()
        projects = [] 
        for project in get_projects: 
            get_p = await crud.get_project(_id=project.parent,session=session)
            if get_p is not None:
                projects.append({'relation_id':project.id,'name':get_p.name,'desc':get_p.desc}) 
        list.append({'info':language,'related_frameworks':frameworks,'related_projects':projects})
    return {'limit':limit,'offset':offset,'author':author,'list':list}

@router.get("/{_id}")
async def get_language(_id:int,session: Session = Depends(get_db)):
    """
    Get Single Language by <b>ID</b> provided in List Languages
    """
    try:
        language = session.query(models.Languages).get(_id)
        get_frameworks = session.query(models.Frameworks).filter_by(main_lanugage=_id).all()
        frameworks = [] 
        for framework in get_frameworks: 
            get_f = await crud.get_framework(_id=framework.child,session=session)
            if get_f is not None:
                frameworks.append({'text':get_f.text,'classname':get_f.classname}) 
        get_projects = session.query(models.Relations).filter_by(child=_id,relation_type='language',parent_type='project').all()
        projects = [] 
        for project in get_projects: 
            get_p = await crud.get_project(_id=project.child,session=session)
            if get_p is not None:
                projects.append({'name':get_p.name,'desc':get_p.desc}) 
        get_articles = session.query(models.Relations).filter_by(child=_id,relation_type='language',parent_type='article').all()
        articles = []
        for article in get_articles: 
            get_p = await crud.get_article(_id=article.parent,session=session)
            if get_p is not None:
                articles.append({'name':get_p.name,'desc':get_p.desc,'github_url':get_p.github_url}) 

        return {'language':language,'related_frameworks':frameworks,'related_articles':articles,'related_projects':projects}
    except:
        raise HTTPException(500,'Something went wrong')

@router.post("/create")
async def create_language(_language: schemas.LanguageCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        create = await crud.create_languages(_language, session)
        return create
    except:
        raise HTTPException(404,'Something went wrong')

@router.put("/update/{id}")
async def update_languages(id:int,info_update:schemas.LanguageCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)) -> schemas.Language:
    try:
        update = await crud.update_languages(id=id,info_update=info_update,db=session,cuid=check_login.id)
        return update
    except:
        raise HTTPException(404,'Something went wrong')

@router.delete("/delete/{id}")
async def delete_languages(id:int,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        delete = await crud.delete_languages(id=id,db=session,cuid=check_login.id)
        return delete
    except:
        raise HTTPException(404,'Something went wrong')