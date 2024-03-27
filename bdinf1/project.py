from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as fastUIcomponents
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field, parse_obj_as

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType, ptdFormAccounts

app = FastAPI()


SQLALCHEMY_DATABASE_URL = "mssql+pymssql://User411:User411p]+36@192.168.112.103/db22204"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FilterForm(BaseModel):
    country: str = Field(json_schema_extra={
                         'search_url': '/api/forms/search', 'placeholder': 'Filter by Country...'})


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')


class NamesTables(BaseModel):
    name: str


FORMS = ["formAccounts"]
class NamesForms(BaseModel):
    name: str


@app.get("/api/tables/tblClient", response_model=FastUI, response_model_exclude_none=True)
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


@app.get("/api/tables/tblAccount", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(List[pdtAccount], db.query(tblAccount).all())
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='tblAccount', level=2),
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]


@app.get("/api/tables/tblAccountType", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(
        List[pdtAccountType], db.query(tblAccountType).all())
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='tblAccountType', level=2),
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]


@app.get("/api/tables/tblOperation", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(List[pdtOperation], db.query(tblOperation).all())
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='tblOperation', level=2),
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]


@app.get("/api/tables/tblOperationType", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(
        List[pdtOperationType], db.query(tblOperationType).all())
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Link(
                    components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                # renders `<h2>Users</h2>`
                fastUIcomponents.Heading(text='tblOperationType', level=2),
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]


@app.get("/api/main", response_model=FastUI, response_model_exclude_none=True)
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



@app.get("/api/forms/formAccounts", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    accounts = parse_obj_as(List[pdtAccount],db.query(tblAccount).all())

    faccs = []
    for fac in accounts:
        faccs += [ptdFormAccounts(clientFullName= f"{fac.client.txtClientSurname} {fac.client.txtClientName} {fac.client.txtClientSecondName}",typeAccount= fac.account_type.txtAccountTypeName, datAccountBegin= fac.datAccountBegin, txtAccountNumber= fac.txtAccountNumber )]

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




@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Bank Service'))
