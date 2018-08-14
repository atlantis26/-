# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8"\
    .format(settings.DB_USER, settings.DB_PASS, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME)
db = create_engine(DATABASE_URI, encoding="utf-8")
Base = declarative_base()
DBSession = sessionmaker(bind=db)


def to_dict(self):
    # 将sqlAlchemy中的对象转换为dict
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict


def create_tables():
    Base.metadata.create_all(bind=db)
