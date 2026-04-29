from pydantic import BaseModel
from typing import Optional

class TestInsRequest(BaseModel):
    name: str
    age: int

class TestSelReqeust(BaseModel):
    id : int

class TestPutReqeust(BaseModel):
    id : int
    name : str
    age : int
    
class TestPatchReqeust(BaseModel):
    id : int
    name : str | None = None
    age : int | None = None
    
class TestDelReqeust(BaseModel):
    id : int