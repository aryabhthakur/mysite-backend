from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud,models
from database import schemas
from .auth import get_current_active_user
router =  APIRouter()
@router.get("/")
async def get_framework_list(limit:int,offset:int,author:int = None,session: Session = Depends(get_db)):
    list = []
    if author is not None:
        frameworks = session.query(models.Frameworks).filter_by(author_id=author).limit(limit).offset(offset).all()
    else:
        frameworks = session.query(models.Frameworks).limit(limit).offset(offset).all()
    for framework in frameworks:
        language = await crud.get_language(_id=framework.main_lanugage,session=session) #type:ignore
        get_projects = session.query(models.Relations).filter_by(child=framework.id,relation_type='framework',parent_type='project').all()
        projects = [] 
        for project in get_projects: 
            get_p = await crud.get_project(_id=project.parent,session=session)
            if get_p is not None:
                projects.append({'name':get_p.name,'desc':get_p.desc,'github_url':get_p.github_url})  
        list.append({'info':framework,'related_language':language,'related_projects':projects})
    return {'limit':limit,'offset':offset,'author':author,'list':list}

@router.get("/{_id}")
async def get_frameworks(_id:int,session: Session = Depends(get_db)):
    """
    Get Single Framework by <b>ID</b> provided in List Frameworks
    """
    framework = session.query(models.Frameworks).get(_id)
    if framework is not None:
        try:
            language = await crud.get_language(_id=framework.main_lanugage,session=session) #type:ignore
            get_projects = session.query(models.Relations).filter_by(child=_id,relation_type='framework',parent_type='project').all()
            projects = [] 
            for project in get_projects: 
                get_p = await crud.get_project(_id=project.parent,session=session)
                if get_p is not None:
                    projects.append({'name':get_p.name,'desc':get_p.desc}) 
            get_articles = session.query(models.Relations).filter_by(child=_id,relation_type='framework',parent_type='article').all()
            articles = []
            for article in get_articles: 
                get_p = await crud.get_article(_id=article.parent,session=session)
                if get_p is not None:
                    articles.append({'name':get_p.name,'desc':get_p.desc,'github_url':get_p.github_url}) 
            return {'framework':framework,'related_language':language,'related_articles':articles,'related_projects':projects}
        except:
            raise HTTPException(500,'Something went wrong')
    else:
         raise HTTPException(404,'Framework not found')

@router.post("/create")
async def create_framework(_framework: schemas.FrameworkCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        create = await crud.create_frameworks(_framework, session)
        return create
    except:
        raise HTTPException(404,'Something went wrong')

@router.put("/update/{id}")
async def update_frameworks(id:int,info_update:schemas.FrameworkCreate,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)) -> schemas.Language:
    try:
        update = await crud.update_frameworks(id=id,info_update=info_update,db=session,cuid=check_login.id)
        return update
    except:
        raise HTTPException(404,'Something went wrong')

@router.delete("/delete/{id}")
async def delete_frameworks(id:int,session: Session = Depends(get_db),check_login: schemas.User = Depends(get_current_active_user)):
    try:
        delete = await crud.delete_frameworks(id=id,db=session,cuid=check_login.id)
        return delete
    except:
        raise HTTPException(404,'Something went wrong')