from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from toolenv import get_dbconf

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation



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


#EVANTS 

def on_operation_insert(mapper, connection, operation):
    session = sessionmaker(bind=connection)()
    account_id = operation.intAccountId
    account = session.query(tblAccount).filter_by(intAccountId=account_id).first()
    if account:
        account.fltAccountSum += operation.fltValue
        session.commit()
    session.close()

# Подписываемся на событие добавления операции
event.listen(tblOperation, 'after_insert', on_operation_insert)


