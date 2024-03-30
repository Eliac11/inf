import dbtools.models as models

from sqlalchemy import create_engine

# engine = create_engine('sqlite:///Bank.db')

connection_string = "mssql+pymssql://User411:User411p]+36@192.168.112.103/db22204"
engine = create_engine(connection_string)

models.Base.metadata.create_all(engine)