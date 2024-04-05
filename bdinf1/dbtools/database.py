from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from toolenv import get_dbconf




SQLALCHEMY_DATABASE_URL = f"mssql+pymssql://{get_dbconf()}?charset=cp1251"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()