from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    description: str
    duration_minutes: int
    genre: str
    language: str
    release_date: str  

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    release_date: Optional[str] = None

class Movie(BaseModel):
    id: str
    title: str
    description: str
    duration_minutes: int
    genre: str
    language: str
    release_date: str