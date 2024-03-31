from sqlalchemy.orm import Session
from typing import List, Annotated
from collections import defaultdict

from fastapi import Depends, APIRouter, Request
from fastapi.responses import FileResponse
from fastui import FastUI, AnyComponent, components as fastUIcomponents
from fastui.events import BackEvent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import parse_obj_as, BaseModel, Field
from fastui.forms import FormFile, SelectSearchResponse, Textarea, fastui_form

from sqlalchemy.orm import Session

from dbtools.models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from dbtools.models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, pdtFormAccounts, NamesForms, NamesTables, FORMS, FormDownloadAccountInfo
from dbtools.database import get_db, metadata

from httpx import AsyncClient

from untilstools.makePDFallAcc import create_reportAllAcc
from untilstools.makePDFendAcc import create_reportEndAcc
from untilstools.makePDFinfoAcc import create_reportinfoAcc


router = APIRouter()


@router.get('/service/downloadFile')
async def search_view(request: Request, reptype: str, account_number: str = None) -> FileResponse:
    file_location = "./tmp/"

    if reptype == "allAcc":
        file_name = create_reportAllAcc()
    elif reptype == "endAcc":
        file_name = create_reportEndAcc()
    elif reptype == "infoAcc" and account_number != None:
        file_name = create_reportinfoAcc(account_number)

    file_location += file_name

    return FileResponse(file_location, media_type='application/octet-stream',filename=file_name)

@router.post('/service/downloadFileFromForm', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(form:Annotated[FormDownloadAccountInfo,fastui_form(FormDownloadAccountInfo)], db: Session = Depends(get_db)):
    account_number = form.account_number
    return [fastUIcomponents.FireEvent(event=GoToEvent(url='/service/downloadFile?reptype=infoAcc&account_number=' + account_number, target="_blank"))]
