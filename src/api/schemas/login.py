from pydantic import BaseModel

class put_shop_item(BaseModel):
    token: str 
    name: str 
    description: str 
    photo: bytes 
    prise: float 
    contacts: str 