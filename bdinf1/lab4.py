from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from models import tblOperation, tblAccount


engine = create_engine('mssql+pymssql://User411:User411p]+36@192.168.112.103/db22204')
Session = sessionmaker(bind=engine)
session = Session()


period1_start = '2022-01-01'
period1_end = '2024-02-01'
period2_start = '2022-05-01'
period2_end = '2024-06-01'


operations = session.query(tblOperation).join(tblAccount).filter(
    or_(
        and_(
            tblOperation.datOperation >= period1_start,
            tblOperation.datOperation <= period1_end
        ),
        and_(
            tblOperation.datOperation >= period2_start,
            tblOperation.datOperation <= period2_end
        )
    ),
    tblOperation.fltValue >= 200,
    tblOperation.fltValue <= 1000
).order_by(tblOperation.datOperation).all()

print("Result:")
for operation in operations:
    print(f"Номер счета: {operation.account.txtAccountNumber}, Дата проведения операции: {operation.datOperation}, Сумма операции: {operation.fltValue}")
