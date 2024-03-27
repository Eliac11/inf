from sqlalchemy.orm import Session
from typing import List

from fastapi import Depends, APIRouter
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from pydantic import parse_obj_as

from sqlalchemy.orm import Session

from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, ptdFormAccounts, NamesForms, NamesTables
from database import get_db


router = APIRouter()

@router.get("/api/tables/tblClient", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(List[pdtClient], db.query(tblClient).all())

    return [
        fastUIcomponents.Page(
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                fastUIcomponents.Heading(text='tblClient', level=2),
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]