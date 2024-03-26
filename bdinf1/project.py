from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as fastUIcomponents
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field, parse_obj_as

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import tblClient, tblAccountType, tblAccount, tblOperationType, tblOperation
from models_pydentic import pdtAccount, pdtClient, pdtAccountType, pdtOperation, pdtOperationType

app = FastAPI()


SQLALCHEMY_DATABASE_URL = "mssql+pymssql://User411:User411p]+36@192.168.112.103/db22204"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# print(pdtClient.model_validate(next(get_db()).query(tblClient).all()[0]))

class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')


# define some users
users = [
    User(id=1, name='John', dob=date(1990, 1, 1)),
    User(id=2, name='Jack', dob=date(1991, 1, 1)),
    User(id=3, name='Jill', dob=date(1992, 1, 1)),
    User(id=4, name='Jane', dob=date(1993, 1, 1)),
]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text='Users', level=2),  # renders `<h2>Users</h2>`
                fastUIcomponents.Table(
                    data=users,
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field='dob', mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]


@app.get("/api/bankUsers", response_model=FastUI, response_model_exclude_none=True)
def users_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    bankusers = parse_obj_as(List[pdtClient], db.query(tblClient).all())
    return [
        fastUIcomponents.Page(  # Page provides a basic container for components
            components=[
                fastUIcomponents.Heading(text='BankUsersUsers', level=2),  # renders `<h2>Users</h2>`
                fastUIcomponents.Table(
                    data=bankusers
                ),
            ]
        ),
    ]


@app.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(user_id: int) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """
    try:
        user = next(u for u in users if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        fastUIcomponents.Page(
            components=[
                fastUIcomponents.Heading(text=user.name, level=2),
                fastUIcomponents.Link(components=[fastUIcomponents.Text(text='Back')], on_click=BackEvent()),
                fastUIcomponents.Details(data=user),
            ]
        ),
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))