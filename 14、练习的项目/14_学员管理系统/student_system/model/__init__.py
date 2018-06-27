# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

DATABASE_URI = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'\
            .format(settings.DB_USER, settings.DB_PASS, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME)
db = create_engine(DATABASE_URI, pool_size=100, max_overflow=200, pool_recycle=3600)

BaseModel = declarative_base()
BaseModel.metadata.create_all(bind=db)
DBSession = sessionmaker(bind=db)
