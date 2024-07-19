from pydantic import BaseModel
from fastapi import UploadFile, File

class put_update_item(BaseModel):
    token: str
    name: str
    short_description: str
    full_description: str
    price: float
    contacts: str
    last_photos: str | None = None
    new_photos: list[UploadFile] | None = None