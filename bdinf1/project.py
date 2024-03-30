from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as fastUIcomponents
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field, parse_obj_as

from sqlalchemy.orm import Session

from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, ptdFormAccounts, NamesForms, NamesTables
from models_pydentic import FORMS
from database import get_db, metadata

from routes.tables import rtstblAccount, rtstblClient, rtstblAccountType, rtstblOperation, rtstblOperationType
from routes import rtsmain
from routes.forms import rtsformAccounts, rtsformNewAccount
from routes.service import rtsSerchAcountsType, rtsSerchClients

app = FastAPI()

#main
app.include_router(rtsmain.router)

#tables
app.include_router(rtstblClient.router)
app.include_router(rtstblAccount.router)
app.include_router(rtstblAccountType.router)
app.include_router(rtstblOperation.router)
app.include_router(rtstblOperationType.router)

#forms
app.include_router(rtsformAccounts.router)
app.include_router(rtsformNewAccount.router)

#services
app.include_router(rtsSerchAcountsType.router)
app.include_router(rtsSerchClients.router)

@app.get('/api/')
async def gotomain():
    return [fastUIcomponents.FireEvent(event=GoToEvent(url='/main'))]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Bank Service'))
