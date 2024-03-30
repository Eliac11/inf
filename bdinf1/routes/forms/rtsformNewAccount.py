from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import date

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from pydantic import parse_obj_as, BaseModel, Field, validator

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS
from dbtools.database import get_db , metadata


router = APIRouter()


class SelectForm(BaseModel):
    intAccountTypeId: str = Field(json_schema_extra={'search_url': '/service/searchAcountsType'}, title="Account Type")
    intClientId: str = Field(json_schema_extra={'search_url': '/service/serchClients'}, title="Client name")
    datAccountBegin: date = Field(title='Account Begin')
    datAccountEnd: date = Field(title='Account End')
    txtAccountNumber: str = Field(max_length=10, min_length=10, pattern=r"[0-9]", title='Account Number')
    fltAccountSum: int = Field(title='Account Sum')

    @validator('datAccountEnd')
    def validate_datAccountEnd(cls, value, values):
        if 'datAccountBegin' in values and value <= values['datAccountBegin']:
            raise ValueError('Account End date must be greater than Account Begin date')
        return value

    

@router.get("/api/forms/formNewAccounts", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:

    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text='New Account', level= 1),
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                fastUIcomponents.Heading(text='Create new account', level = 2),
                fastUIcomponents.ModelForm(model=SelectForm, display_mode='page', submit_url='/api/forms/formNewAccounts'),
            ])
        ]



@router.post('/api/forms/formNewAccounts', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(form: Annotated[SelectForm, fastui_form(SelectForm)], db: Session = Depends(get_db)):

    account = tblAccount(
        intAccountTypeId=form.intAccountTypeId,
        intClientId=form.intClientId,
        datAccountBegin=form.datAccountBegin,
        datAccountEnd=form.datAccountEnd,
        txtAccountNumber=form.txtAccountNumber,
        fltAccountSum=form.fltAccountSum
    )
    db.add(account)
    db.commit()
    return [fastUIcomponents.FireEvent(event=GoToEvent(url='/forms/formAccounts'))]