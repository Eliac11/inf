from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta
from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation


# engine = create_engine('sqlite:///Bank.db')
connection_string = "mssql+pymssql://User411:User411p]+36@192.168.112.103/db22204"
engine = create_engine(connection_string)


Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


for _ in range(10):
    client = tblClient(
        txtClientSurname=fake.last_name(),
        txtClientName=fake.first_name(),
        txtClientSecondName=fake.last_name(),
        datBirthday=fake.date_of_birth(),
        txtClientAddress=fake.address()
    )
    session.add(client)

for _ in range(10):
    account_type = tblAccountType(
        txtAccountTypeName=fake.word(),
        txtAccountTypeComment=fake.sentence()
    )
    session.add(account_type)

for _ in range(30):
    operation_type = tblOperationType(
        txtOperationTypeName=fake.word()
    )
    session.add(operation_type)

session.commit()


client_ids = [client.intClientId for client in session.query(tblClient)]
account_type_ids = [account_type.intAccountTypeId for account_type in session.query(tblAccountType)]
operation_type_ids = [operation_type.intOperationTypeId for operation_type in session.query(tblOperationType)]

for _ in range(30):
    account = tblAccount(
        intAccountTypeId=choice(account_type_ids),
        intClientId=choice(client_ids),
        datAccountBegin=fake.date_between(start_date='-1y', end_date='today'),
        datAccountEnd=fake.date_between(start_date='today', end_date='+1y'),
        txtAccountNumber=fake.random_int(min=1000000000, max=9999999999),
        fltAccountSum=randint(1000, 100000)
    )
    session.add(account)

account_ids = [account.intAccountId for account in session.query(tblAccount)]

for _ in range(30):
    operation = tblOperation(
        intOperationTypeId=choice(operation_type_ids),
        intAccountId=choice(account_ids),
        fltValue=randint(10, 10000),
        datOperation=fake.date_time_between(start_date='-1y', end_date='now')
    )
    session.add(operation)

session.commit()
