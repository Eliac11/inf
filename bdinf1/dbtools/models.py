from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker



Base = declarative_base()

class tblClient(Base):
    __tablename__ = 'tblClient'
    intClientId = Column(Integer, primary_key=True)
    txtClientSurname = Column(String(30))
    txtClientName = Column(String(25))
    txtClientSecondName = Column(String(30))
    datBirthday = Column(Date)
    txtClientAddress = Column(String(100))
    accounts = relationship('tblAccount', back_populates='client')

class tblAccountType(Base):
    __tablename__ = 'tblAccountType'
    intAccountTypeId = Column(Integer, primary_key=True)
    txtAccountTypeName = Column(String(100))
    txtAccountTypeComment = Column(String(255))
    accounts = relationship('tblAccount', back_populates='account_type')

class tblAccount(Base):
    __tablename__ = 'tblAccount'
    intAccountId = Column(Integer, primary_key=True)
    intAccountTypeId = Column(Integer, ForeignKey('tblAccountType.intAccountTypeId'))
    intClientId = Column(Integer, ForeignKey('tblClient.intClientId'))
    datAccountBegin = Column(Date)
    datAccountEnd = Column(Date)
    txtAccountNumber = Column(String(20))
    fltAccountSum = Column(Float)
    client = relationship('tblClient', back_populates='accounts')
    account_type = relationship('tblAccountType', back_populates='accounts')
    operations = relationship('tblOperation', back_populates='account')

class tblOperationType(Base):
    __tablename__ = 'tblOperationType'
    intOperationTypeId = Column(Integer, primary_key=True)
    txtOperationTypeName = Column(String(50))
    operations = relationship('tblOperation', back_populates='operation_type')

class tblOperation(Base):
    __tablename__ = 'tblOperation'
    intOperationId = Column(Integer, primary_key=True)
    intOperationTypeId = Column(Integer, ForeignKey('tblOperationType.intOperationTypeId'))
    intAccountId = Column(Integer, ForeignKey('tblAccount.intAccountId'))
    fltValue = Column(Float)
    datOperation = Column(Date)
    account = relationship('tblAccount', back_populates='operations')
    operation_type = relationship('tblOperationType', back_populates='operations')

