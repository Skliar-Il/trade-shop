from pydantic import BaseModel
from fastapi import UploadFile, File

class post_new_item(BaseModel):
    token: str 
    name: str 
    full_description: str 
    short_description: str
    prise: float 
    contacts: str
    photos: list[UploadFile] = File(...)
    
class delete_item(BaseModel): 
    token: str 