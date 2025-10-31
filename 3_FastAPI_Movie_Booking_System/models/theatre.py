from pydantic import BaseModel
from typing import Optional, List

class TheatreCreate(BaseModel):
    name: str
    location: str
    city: str

class TheatreUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None

class Theatre(BaseModel):
    id: str
    name: str
    location: str
    city: str

class ScreenCreate(BaseModel):
    name: str
    theatre_id: str

class ScreenUpdate(BaseModel):
    name: Optional[str] = None

class Screen(BaseModel):
    id: str
    name: str
    theatre_id: str

class SeatCreate(BaseModel):
    seat_numbers: List[str]  

class ShowCreate(BaseModel):
    movie_id: str
    screen_id: str
    show_date: str  
    show_time: str  
    price: float

class Show(BaseModel):
    id: str
    movie_id: str
    screen_id: str
    show_date: str
    show_time: str
    price: float
    available_seats: List[str]