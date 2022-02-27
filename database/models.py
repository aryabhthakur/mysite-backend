from datetime import date
from sqlalchemy import Boolean, Column, Date, Integer, Numeric, String

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean)


class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(2048))
    author_id = Column(Integer)
    created_on =  Column(Date, default=date.today())

class Languages(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True,index=True)
    text = Column(String(255))
    classname = Column(String(255))
    author_id = Column(Integer)

class Frameworks(Base):
    __tablename__ = "frameworks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    classname = Column(String(255))
    main_lanugage = Column(Integer)
    author_id = Column(Integer)


class Medias(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    type = Column(String(255))
    usage = Column(Integer)
    author_id = Column(Integer)

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    desc = Column(String(255))
    github_url = Column(String(255))
    package_manager = Column(String(255))
    package_manager_url = Column(String(255))
    changelog = Column(String(255))
    version = Column(Numeric)
    author_id = Column(Integer)
    created_on =  Column(Date)
    last_updated_on =  Column(Date)

class Relations(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)
    parent = Column(Integer)
    parent_type = Column(String(255))
    child = Column(Integer)
    relation_type = Column(String(255))
    author_id = Column(Integer)
    current_status = Column(Boolean)
