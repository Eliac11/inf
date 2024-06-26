from sqlalchemy.orm import Session
from typing import List
from collections import defaultdict

from fastapi import Depends, APIRouter, Request
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import parse_obj_as, BaseModel, Field
from fastui.forms import FormFile, SelectSearchResponse, Textarea, fastui_form

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS
from dbtools.database import get_db, metadata

from httpx import AsyncClient


router = APIRouter()


@router.get('/service/searchOperationType', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str, db: Session = Depends(get_db)) -> SelectSearchResponse:

    data = []
    atypes = db.query(tblOperationType).all()
    for i in atypes:
        ditem = {"label":i.txtOperationTypeName, "value": str(i.intOperationTypeId)}
        data.append(ditem)

    blocks = {}
    blocks["Операции"] = data
    options = [{'label': k, 'options': v} for k, v in blocks.items()]
    return SelectSearchResponse(options=options)
