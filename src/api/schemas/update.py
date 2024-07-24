from pydantic import BaseModel, model_validator
from fastapi import UploadFile, File
import json

class put_update_item(BaseModel):
    token: str
    name: str
    short_description: str
    full_description: str
    price: float
    contacts: str
    last_photos: list[str]
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    