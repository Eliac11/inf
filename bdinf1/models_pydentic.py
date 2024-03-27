from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


FORMS = ["formAccounts"]

class pdtClient(BaseModel):
    intClientId: Optional[int]
    txtClientSurname: str
    txtClientName: str
    txtClientSecondName: str
    datBirthday: date
    txtClientAddress: str

    class Config:
        from_attributes = True


class pdtAccountType(BaseModel):
    intAccountTypeId: Optional[int]
    txtAccountTypeName: str
    txtAccountTypeComment: str

    class Config:
        from_attributes = True


class pdtAccount(BaseModel):
    intAccountId: Optional[int]
    intAccountTypeId: int
    intClientId: int
    datAccountBegin: date
    datAccountEnd: date
    txtAccountNumber: str
    fltAccountSum: float
    client: pdtClient
    account_type: pdtAccountType

    class Config:
        from_attributes = True


class pdtOperationType(BaseModel):
    intOperationTypeId: Optional[int]
    txtOperationTypeName: str

    class Config:
        from_attributes = True


class pdtOperation(BaseModel):
    intOperationId: Optional[int]
    intOperationTypeId: int
    intAccountId: int
    fltValue: float
    datOperation: date
    account: pdtAccount
    operation_type: pdtOperationType

    class Config:
        from_attributes = True



class ptdFormAccounts(BaseModel):
    clientFullName: str
    typeAccount: str
    datAccountBegin: date
    txtAccountNumber: str


class NamesTables(BaseModel):
    name: str





class NamesForms(BaseModel):
    name: str
