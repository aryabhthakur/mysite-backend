from .schemas import *
from .models import *
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from exceptions import InfoNotFoundError,NotAuthorizedError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(user: UserCreate,db: Session):
    db_user = Users(email=user.email, hashed_password=get_password_hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_articles(_article: ArticleCreate,db: Session):
    article = Articles(**_article.dict())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

async def delete_articles(id:int,db: Session,cuid:int):
    article = db.query(Articles).get(id)
    if article is None:
        raise InfoNotFoundError
    if cuid == article.author_id:
        db.delete(article)
        db.commit()
        return {'deleted':id}
    else:
        raise NotAuthorizedError

async def update_articles(id:int,info_update:ArticleCreate,db: Session,cuid:int):
    article = db.query(Articles).get(id)
    if article is None:
        raise InfoNotFoundError
    if cuid == article.author_id:
        article.title = info_update.title #type:ignore
        article.content = info_update.content #type:ignore
        article.author_id = info_update.author_id #type:ignore
        db.commit()
        db.refresh(article)
        return article
    else:
        raise NotAuthorizedError

async def create_projects(_projects: ProjectCreate,db: Session):
    d = _projects.dict()
    del d['related_frameworks']
    del d['related_languages']
    project = Projects(**d)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

async def delete_projects(id:int,db: Session,cuid:int):
    project = db.query(Projects).get(id)
    if project is None:
        raise InfoNotFoundError
    if cuid == project.author_id:
        db.delete(project)
        db.commit()
        return {'deleted':id}
    else:
        raise NotAuthorizedError

async def update_projects(id:int,info_update:ProjectCreate,db: Session,cuid:int):
    project = db.query(Projects).get(id)
    if project is None:
        raise InfoNotFoundError
    if cuid == project.author_id:
        project.name = info_update.name #type:ignore
        project.desc = info_update.desc #type:ignore
        project.github_url = info_update.github_url #type:ignore
        project.package_manager = info_update.package_manager #type:ignore
        project.package_manager_url = info_update.package_manager_url #type:ignore
        project.version = info_update.version #type:ignore
        project.changelog = info_update.changelog #type:ignore
        project.created_on = info_update.created_on #type:ignore
        project.last_updated_on = info_update.last_updated_on #type:ignore
        db.commit()
        db.refresh(project)
        return project
    else:
        raise NotAuthorizedError

async def create_languages(_languages: LanguageCreate,db: Session):
    languages = Languages(**_languages.dict())
    db.add(languages)
    db.commit()
    db.refresh(languages)
    return languages

async def delete_languages(id:int,db: Session,cuid:int):
    languages = db.query(Languages).get(id)
    if languages is None:
        raise InfoNotFoundError
    if cuid == languages.author_id:
        db.delete(languages)
        db.commit()
        return {'deleted':id}
    else:
        raise NotAuthorizedError

async def update_languages(id:int,info_update:LanguageCreate,db: Session,cuid:int):
    languages = db.query(Languages).get(id)
    if languages is None:
        raise InfoNotFoundError
    if cuid == languages.author_id:
        languages.text = info_update.text #type:ignore
        languages.classname = info_update.classname #type:ignore
        db.commit()
        db.refresh(languages)
        return languages
    else:
        raise NotAuthorizedError

async def create_frameworks(_frameworks: FrameworkCreate,db: Session):
    framework = Frameworks(**_frameworks.dict())
    db.add(framework)
    db.commit()
    db.refresh(framework)
    return framework

async def delete_frameworks(id:int,db: Session,cuid:int):
    framework = db.query(Frameworks).get(id)
    if framework is None:
        raise InfoNotFoundError
    if cuid == framework.author_id:
        db.delete(framework)
        db.commit()
        return {'deleted':id}
    else:
        raise NotAuthorizedError

async def update_frameworks(id:int,info_update:FrameworkCreate,db: Session,cuid:int):
    framework = db.query(Frameworks).get(id)
    if framework is None:
        raise InfoNotFoundError
    if cuid == framework.author_id:
        framework.text = info_update.text #type:ignore
        framework.classname = info_update.classname #type:ignore
        framework.main_lanugage = info_update.main_lanugage #type:ignore
        db.commit()
        db.refresh(framework)
        return framework
    else:
        raise NotAuthorizedError

async def create_relations(_relation: RelationCreate,db: Session):
    if isinstance(_relation,dict):
        relation = Relations(**_relation)
    else: 
        relation = Relations(**_relation.dict())
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation

async def delete_relations(id:int,db: Session,cuid:int):
    relation = db.query(Relations).get(id)
    if relation is None:
        raise InfoNotFoundError
    if cuid == relation.author_id:
        db.delete(relation)
        db.commit()
        return {'deleted':id}
    else:
        raise NotAuthorizedError

async def update_relations(id:int,info_update:RelationCreate,db: Session,cuid:int):
    relation = db.query(Frameworks).get(id)
    if relation is None:
        raise InfoNotFoundError
    if cuid == relation.author_id:
        relation.parent = info_update.parent #type:ignore
        relation.parent_type = info_update.parent_type #type:ignore
        relation.child = info_update.child #type:ignore
        relation.relation_type = info_update.relation_type #type:ignore
        relation.current_status = info_update.current_status
        db.commit()
        db.refresh(relation)
        return relation
    else:
        raise NotAuthorizedError

async def get_framework(_id:int, session:Session):
    data = session.query(Frameworks).options().get(_id)
    if data is not None: return data

async def get_language(_id:int, session:Session):
    data = session.query(Languages).options().get(_id)
    if data is not None: return data

async def get_project(_id:int, session:Session):
    data = session.query(Projects).options().get(_id)
    if data is not None: return data

async def get_article(_id:int, session:Session):
    data = session.query(Articles).options().get(_id)
    if data is not None: return data

async def get_media(_id:int, session:Session):
    data = session.query(Medias).options().get(_id)
    if data is not None: return data