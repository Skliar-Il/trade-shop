from pydantic import BaseModel


class post_new_item(BaseModel):
    token: str 
    name: str 
    description: str 
    photo: bytes 
    prise: float 
    contacts: str 
    
class delete_item(BaseModel): 
    token: str 