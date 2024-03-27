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
                )
            ]
        ),
    ]