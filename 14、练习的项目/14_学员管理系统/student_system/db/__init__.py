# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8"\
    .format(settings.DB_USER, settings.DB_PASS, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME)
db = create_engine(DATABASE_URI, encoding="utf-8")
BaseModel = declarative_base()
DBSession = sessionmaker(bind=db)


def create_tables():
    BaseModel.metadata.create_all(bind=db)
