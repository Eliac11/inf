
from datetime import date
from pydantic import parse_obj_as, BaseModel, Field, validator

from dbtools.database import get_db


class SelectForm(BaseModel):
    intOperationTypeId: str = Field(json_schema_extra={
                                    'search_url': '/service/searchOperationType'}, title="Тип операции")
    datOperation: date = Field(title='Дата орерации')
    fltValue: int = Field(title='Сумма', description="")

    
