from pydantic import BaseModel, model_validator
import json

class post_new_item(BaseModel):
    token: str
    name: str
    description: str
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    
class delete_item(BaseModel): 
    token: str 