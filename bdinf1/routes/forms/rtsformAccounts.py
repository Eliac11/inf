from sqlalchemy.orm import Session
from typing import List

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import parse_obj_as

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS
from dbtools.database import get_db , metadata

router = APIRouter()


@router.get("/api/forms/Счета", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    qacc = db.query(tblAccount).all()
    if len(qacc) > 0:
        accounts = parse_obj_as(List[pdtAccount], qacc)
    else:
        accounts = []

    faccs = []
    for fac in accounts:
        faccs += [pdtFormAccounts(clientFullName=f"{fac.client.txtClientSurname} {fac.client.txtClientName} {fac.client.txtClientSecondName}",
                                  typeAccount=fac.account_type.txtAccountTypeName, datAccountBegin=fac.datAccountBegin, txtAccountNumber=fac.txtAccountNumber, intAccountId=fac.intAccountId)]

    if len(faccs) > 0:
        tablepos = fastUIcomponents.Table(
                    data=faccs,
                    columns=[
                        DisplayLookup(field="clientFullName", title="ФИО владельца"),
                        DisplayLookup(field="typeAccount", title="тип счета"),
                        DisplayLookup(field="datAccountBegin", title="дата открытия"),
                        DisplayLookup(field="txtAccountNumber", title="Номер счета" ,on_click=GoToEvent(url="/forms/formAccountInfo?account_id={intAccountId}")),
                    ]
                )
    else:
        tablepos = fastUIcomponents.Heading(text='Счетов нет', level=2)

    return [
        
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Назад')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='Все счета', level=2),
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Создать новый счет')], on_click=GoToEvent(url='/forms/formNewAccounts')),
                tablepos,
            ]
        ),
    ]