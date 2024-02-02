from pydantic import BaseModel


class SpecialSchema(BaseModel):
    special_id: str
    name: str
    ref: str
    img_ref: str
    type: str