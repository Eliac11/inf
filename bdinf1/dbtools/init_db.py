import models as models

from sqlalchemy import create_engine
# from toolenv import get_dbconf

# engine = create_engine('sqlite:///Bank.db')

# connection_string = f"mssql+pymssql://{get_dbconf()}?charset=utf8"
connection_string = f"sqlite:///./test.db"
engine = create_engine(connection_string)

models.Base.metadata.create_all(engine)