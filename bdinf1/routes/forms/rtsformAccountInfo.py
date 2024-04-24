from sqlalchemy.orm import Session
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import parse_obj_as
from sqlalchemy.exc import OperationalError

from sqlalchemy.orm import Session
from sqlalchemy import text

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
                                                fastUIcomponents.Heading(text="Операции", level=3),
                                                fastUIcomponents.Table(
                                                        data=operations,
                                                        columns=[
                                                            DisplayLookup(field='datOperation', title="Дата орепации"),
                                                            DisplayLookup(field='operation_type', title="Тип"),
                                                            DisplayLookup(field='fltValue', title="Сумма", on_click=GoToEvent(url="/forms/delOperation?intOperationId={intOperationId}"))
                                                        ]
                                                    )
                                                ]
                )
    else:
        tableview = fastUIcomponents.Heading(text = "Нет операций", level=3)

    clientfullname = f"{acc.client.txtClientSurname} {acc.client.txtClientName} {acc.client.txtClientSecondName}"
    acctype = f"{acc.account_type.txtAccountTypeName}"
    cardInfo = fastUIcomponents.Div(
        class_name="border mt-3 pt-1",
        components=[
            fastUIcomponents.Heading(text=f"ID:              {acc.intAccountId}",level=4),
            fastUIcomponents.Heading(text=f"Тип:            {acctype}",level=4),
            fastUIcomponents.Heading(text=f"ФИО: {clientfullname}",level=4),
            fastUIcomponents.Heading(text=f"Дата открытия:    {acc.datAccountBegin}",level=4),
            fastUIcomponents.Heading(text=f"Дата закрытия:      {acc.datAccountEnd}",level=4),
            fastUIcomponents.Heading(text=f"Номер счета:   {acc.txtAccountNumber}",level=4),
            fastUIcomponents.Heading(text=f"Баланс:      {acc.fltAccountSum}",level=4),
        ]
        )


    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text="Информация счета", level= 1),
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Назад')], on_click=BackEvent()),
                cardInfo,
                tableview,
                fastUIcomponents.Button(text='Добавиить новую операцию', on_click=PageEvent(name='open-form')),
                fastUIcomponents.Modal(
                    title='Добавить новую операцию',
                    body=[
                        fastUIcomponents.Paragraph(text=clientfullname),
                        fastUIcomponents.Paragraph(text=acctype),
                        fastUIcomponents.ModelForm(model=formNewOperation.SelectForm, display_mode='default', submit_url=f"/api/forms/formNewOperation?account_id={account_id}", submit_trigger=PageEvent(name='submit-form')),
                    ],
                    open_trigger=PageEvent(name='open-form')
                )
            ]
        ),
    ]


@router.post('/api/forms/formNewOperation', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(account_id: int, form: Annotated[formNewOperation.SelectForm, fastui_form(formNewOperation.SelectForm)], db: Session = Depends(get_db)):

    sql_query = text("INSERT INTO tblOperation (intOperationTypeId, intAccountId, fltValue, datOperation) VALUES (:type_id, :account_id, :value, :operation_date)")

    
    

    try:
        db.execute(sql_query, {
        'type_id': int(form.intOperationTypeId),
        'account_id': account_id,
        'value': form.fltValue,
        'operation_date': form.datOperation
    })
        db.commit()
        return [fastUIcomponents.FireEvent(event=PageEvent(name='open-form', clear=True)),
                fastUIcomponents.FireEvent(event=GoToEvent(url=f"/forms/formAccountInfo?account_id={account_id}"))]
    except OperationalError:
        raise HTTPException(status_code=422, detail={
                                    "form": [
                                        {
                                            "type": "value_error",
                                            "loc": [
                                                "datOperation"
                                            ],
                                            "msg": "В этот день уже была проведена операция"
                                        }
                                    ]
                                }
                            
                        )

@router.get('/api/forms/delOperation', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(intOperationId: int, db: Session = Depends(get_db)):

    operation = db.query(tblOperation).filter(tblOperation.intOperationId == intOperationId).first()
    accid = int(operation.intAccountId)

    db.delete(operation)
    db.commit()
    return [fastUIcomponents.FireEvent(event=GoToEvent(url=f"/forms/formAccountInfo?account_id={accid}"))]

