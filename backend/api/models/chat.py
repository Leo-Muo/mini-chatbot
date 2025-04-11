from pydantic import BaseModel, Field, field_validator
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('api/.env')
load_dotenv(dotenv_path=dotenv_path)

max_length = int(os.getenv("MAX_LENGTH"))

class ChatRequest(BaseModel):
    message: str = Field(max_length=max_length)
    
    @field_validator('message')
    def validate_message(cls, v):
        if len(v) > max_length:
            raise ValueError(f"Message must be no more than {max_length} characters long")
        return v

