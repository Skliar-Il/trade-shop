from pydantic import BaseModel, model_validator
from fastapi import UploadFile, File
from typing import List
import json

class update_shop_item(BaseModel):
    token: str
    name: str
    short_description: str
    full_description: str
    price: float
    contacts: str
    last_photos: List[str] | None = None
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
class update_blog_item(BaseModel):
    token: str
    name: str
    description: str
    last_photos: List[str] | None = None
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    