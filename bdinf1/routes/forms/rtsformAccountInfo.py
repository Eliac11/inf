from sqlalchemy.orm import Session
from typing import List, Annotated

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import parse_obj_as

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS
from dbtools.database import get_db , metadata

from routes.forms import formNewOperation

router = APIRouter()

@router.get("/api/forms/formAccountInfo", response_model=FastUI, response_model_exclude_none=True)
def users_table(account_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    acc = db.query(tblAccount).filter(tblAccount.intAccountId == account_id).first()
    
    queryoperations = list(db.query(tblOperation).filter(tblOperation.intAccountId == acc.intAccountId))
    if queryoperations:
        operations = parse_obj_as(List[pdtOperation], db.query(tblOperation).filter(tblOperation.intAccountId == acc.intAccountId))
        tableview = fastUIcomponents.Div(class_name='border-top mt-3 pt-1', 
                                            components= [
                                                fastUIcomponents.Heading(text="Operations", level=3),
                                                fastUIcomponents.Table(
                                                        data=operations,
                                                        columns=[
                                                            DisplayLookup(field='datOperation'),
                                                            DisplayLookup(field='operation_type'),
                                                            DisplayLookup(field='fltValue')
                                                        ]
                                                    )
                                                ]
                )
    else:
        tableview = fastUIcomponents.Heading(text = "Not Operations", level=3)

    clientfullname = f"{acc.client.txtClientSurname} {acc.client.txtClientName} {acc.client.txtClientSecondName}"
    acctype = f"{acc.account_type.txtAccountTypeName}"
    cardInfo = fastUIcomponents.Div(
        class_name="border mt-3 pt-1",
        components=[
            fastUIcomponents.Heading(text=f"ID:              {acc.intAccountId}",level=4),
            fastUIcomponents.Heading(text=f"Type:            {acctype}",level=4),
            fastUIcomponents.Heading(text=f"Client Fullname: {clientfullname}",level=4),
            fastUIcomponents.Heading(text=f"AccountBegin:    {acc.datAccountBegin}",level=4),
            fastUIcomponents.Heading(text=f"AccountEnd:      {acc.datAccountEnd}",level=4),
            fastUIcomponents.Heading(text=f"AccountNumber:   {acc.txtAccountNumber}",level=4),
            fastUIcomponents.Heading(text=f"AccountSum:      {acc.fltAccountSum}",level=4),
        ]
        )


    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text="Account Info", level= 1),
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                cardInfo,
                tableview,
                fastUIcomponents.Button(text='Add New Operations', on_click=PageEvent(name='open-form')),
                fastUIcomponents.Modal(
                    title='Add Operations',
                    body=[
                        fastUIcomponents.Paragraph(text=clientfullname),
                        fastUIcomponents.Paragraph(text=acctype),
                        fastUIcomponents.ModelForm(model=formNewOperation.SelectForm, display_mode='default', submit_url=f"/api/forms/formNewOperation?account_id={account_id}", submit_trigger=PageEvent(name='submit-form'), submit_on_change=True),
                    ],
                    open_trigger=PageEvent(name='open-form')
                )
            ]
        ),
    ]


@router.post('/api/forms/formNewOperation', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(account_id: int, form: Annotated[formNewOperation.SelectForm, fastui_form(formNewOperation.SelectForm)], db: Session = Depends(get_db)):

    operation = tblOperation(
        intOperationTypeId = form.intOperationTypeId,
        intAccountId = account_id,
        fltValue = form.fltValue,
        datOperation = form.datOperation,
    )
    db.add(operation)
    db.commit()
    return [fastUIcomponents.FireEvent(event=PageEvent(name='open-form', clear=True)),
            fastUIcomponents.FireEvent(event=GoToEvent(url=f"/forms/formAccountInfo?account_id={account_id}"))]

