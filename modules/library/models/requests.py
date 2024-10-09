from pydantic import BaseModel, Field, validator
from typing import Optional
from modules.library.models.models import UserRoles
import re
from werkzeug.security import generate_password_hash

class SignUpRequest(BaseModel):
    username: str
    password: str
    role: UserRoles
    first_name: str
    last_name: str 

    @validator('password')
    def validate_password(cls, v, values, **kwargs):
        password_pattern = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,}$")
        if not password_pattern.match(v):
            raise ValueError('Password must be at least 8 characters long, contain at least one digit, one special character, and one capital letter')
        return v

    @validator('password', always=True)
    def hash_password(cls, v):
        return generate_password_hash(v)

    