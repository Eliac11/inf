from sqlalchemy.orm import Session
from typing import List

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import parse_obj_as, Field
import pydantic

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS, FormDownloadAccountInfo
from dbtools.database import get_db , metadata


router = APIRouter()




@router.get("/api/main", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    table_names = [NamesTables(name=tname) for tname in metadata.tables.keys()]

    forms = [NamesForms(name=fname) for fname in FORMS]

    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text='Tables', level=2),
                fastUIcomponents.Table(
                    data=table_names,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(
                            url='/tables/{name}')),
                    ],
                ),
                fastUIcomponents.Heading(text='Forms', level=2),
                fastUIcomponents.Table(
                    data=forms,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(
                            url='/forms/{name}')),
                    ],
                ),
                fastUIcomponents.Div(
                    class_name='border-top mt-3 pt-1',
                    components=[
                        fastUIcomponents.Heading(text='Reports', level=2),
                        fastUIcomponents.Button(text="Report Accounts", on_click=GoToEvent(url='/service/downloadFile?reptype=allAcc', target='_blank')),
                        fastUIcomponents.Button(text="Report End Accounts", class_name='+ ms-4', on_click=GoToEvent(url='/service/downloadFile?reptype=endAcc', target='_blank')),
                        fastUIcomponents.ModelForm(
                                            model=FormDownloadAccountInfo,
                                            submit_url='/service/downloadFileFromForm',
                                            method='POST',
                                            submit_on_change=True,
                                            display_mode='inline',
                                            class_name="row row-cols-lg-4 align-items-center justify-content-start mt-4"
                                        )
                    ]
                )
            ]
        ),
    ]