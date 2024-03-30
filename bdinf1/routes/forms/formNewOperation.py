
from datetime import date
from pydantic import parse_obj_as, BaseModel, Field, validator



class SelectForm(BaseModel):
    intOperationTypeId: str = Field(json_schema_extra={'search_url': '/service/searchOperationType'}, title="Operation Type")
    datOperation: date = Field(title='Date Operation')
    fltValue: int = Field(title='Account Sum', description="Example: -100, +100")