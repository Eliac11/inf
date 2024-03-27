from sqlalchemy.orm import Session
from typing import List

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import parse_obj_as

from sqlalchemy.orm import Session

from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, ptdFormAccounts, NamesForms, NamesTables, FORMS
from database import get_db , metadata

router = APIRouter()

@router.get("/api/forms/formAccounts", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    accounts = parse_obj_as(List[pdtAccount], db.query(tblAccount).all())

    faccs = []
    for fac in accounts:
        faccs += [ptdFormAccounts(clientFullName=f"{fac.client.txtClientSurname} {fac.client.txtClientName} {fac.client.txtClientSecondName}",
                                  typeAccount=fac.account_type.txtAccountTypeName, datAccountBegin=fac.datAccountBegin, txtAccountNumber=fac.txtAccountNumber)]

    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='FormAccounts', level=2),
                fastUIcomponents.Table(
                    data=faccs
                ),
            ]
        ),
    ]