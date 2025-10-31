from pydantic import BaseModel
from typing import List

class BookingCreate(BaseModel):
    show_id: str
    seats: List[str]  # e.g., ["A1", "A2"]

class Booking(BaseModel):
    id: str
    user_id: str
    show_id: str
    seats: List[str]
    total_price: float
    booking_date: str
    status: str  # "confirmed" or "cancelled"