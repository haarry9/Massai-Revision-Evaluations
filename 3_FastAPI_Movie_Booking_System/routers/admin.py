from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from models.movie import MovieCreate, MovieUpdate, Movie
from models.theatre import (
    TheatreCreate, TheatreUpdate, Theatre,
    ScreenCreate, ScreenUpdate, Screen,
    SeatCreate, ShowCreate, Show
)
from models.booking import Booking
from database import (
    movies_collection, theatres_collection,
    screens_collection, shows_collection,
    bookings_collection, users_collection
)
from utils.auth import get_current_admin, TokenData

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])

# Theatre Management
@router.post("/theatres", status_code=status.HTTP_201_CREATED)
async def create_theatre(theatre: TheatreCreate):
    theatre_doc = theatre.dict()
    result = await theatres_collection.insert_one(theatre_doc)
    return {"message": "Theatre created", "id": str(result.inserted_id)}

@router.put("/theatres/{theatre_id}")
async def update_theatre(theatre_id: str, theatre: TheatreUpdate):
    if not ObjectId.is_valid(theatre_id):
        raise HTTPException(status_code=400, detail="Invalid theatre ID")
    
    update_data = {k: v for k, v in theatre.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await theatres_collection.update_one(
        {"_id": ObjectId(theatre_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    return {"message": "Theatre updated"}

@router.delete("/theatres/{theatre_id}")
async def delete_theatre(theatre_id: str):
    if not ObjectId.is_valid(theatre_id):
        raise HTTPException(status_code=400, detail="Invalid theatre ID")
    
    result = await theatres_collection.delete_one({"_id": ObjectId(theatre_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    # Also delete associated screens
    await screens_collection.delete_many({"theatre_id": theatre_id})
    
    return {"message": "Theatre deleted"}

# Screen Management
@router.post("/theatres/{theatre_id}/screens", status_code=status.HTTP_201_CREATED)
async def add_screen(theatre_id: str, screen: ScreenCreate):
    if not ObjectId.is_valid(theatre_id):
        raise HTTPException(status_code=400, detail="Invalid theatre ID")
    
    # Check if theatre exists
    theatre = await theatres_collection.find_one({"_id": ObjectId(theatre_id)})
    if not theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    screen_doc = {
        "name": screen.name,
        "theatre_id": theatre_id,
        "seats": []  # Will be populated later
    }
    
    result = await screens_collection.insert_one(screen_doc)
    return {"message": "Screen added", "id": str(result.inserted_id)}

@router.put("/screens/{screen_id}")
async def update_screen(screen_id: str, screen: ScreenUpdate):
    if not ObjectId.is_valid(screen_id):
        raise HTTPException(status_code=400, detail="Invalid screen ID")
    
    update_data = {k: v for k, v in screen.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await screens_collection.update_one(
        {"_id": ObjectId(screen_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    return {"message": "Screen updated"}

@router.delete("/screens/{screen_id}")
async def delete_screen(screen_id: str):
    if not ObjectId.is_valid(screen_id):
        raise HTTPException(status_code=400, detail="Invalid screen ID")
    
    result = await screens_collection.delete_one({"_id": ObjectId(screen_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    return {"message": "Screen deleted"}

# Seat Management
@router.post("/screens/{screen_id}/seats")
async def define_seats(screen_id: str, seat_data: SeatCreate):
    if not ObjectId.is_valid(screen_id):
        raise HTTPException(status_code=400, detail="Invalid screen ID")
    
    result = await screens_collection.update_one(
        {"_id": ObjectId(screen_id)},
        {"$set": {"seats": seat_data.seat_numbers}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    return {"message": "Seats defined successfully"}

# Movie Management
@router.post("/movies", status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieCreate):
    movie_doc = movie.dict()
    result = await movies_collection.insert_one(movie_doc)
    return {"message": "Movie created", "id": str(result.inserted_id)}

@router.put("/movies/{movie_id}")
async def update_movie(movie_id: str, movie: MovieUpdate):
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(status_code=400, detail="Invalid movie ID")
    
    update_data = {k: v for k, v in movie.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await movies_collection.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {"message": "Movie updated"}

@router.delete("/movies/{movie_id}")
async def delete_movie(movie_id: str):
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(status_code=400, detail="Invalid movie ID")
    
    result = await movies_collection.delete_one({"_id": ObjectId(movie_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {"message": "Movie deleted"}

# Show Management
@router.post("/shows", status_code=status.HTTP_201_CREATED)
async def create_show(show: ShowCreate):
    # Validate movie exists
    if not ObjectId.is_valid(show.movie_id):
        raise HTTPException(status_code=400, detail="Invalid movie ID")
    movie = await movies_collection.find_one({"_id": ObjectId(show.movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Validate screen exists
    if not ObjectId.is_valid(show.screen_id):
        raise HTTPException(status_code=400, detail="Invalid screen ID")
    screen = await screens_collection.find_one({"_id": ObjectId(show.screen_id)})
    if not screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    # Get all seats from screen
    available_seats = screen.get("seats", [])
    
    show_doc = {
        "movie_id": show.movie_id,
        "screen_id": show.screen_id,
        "show_date": show.show_date,
        "show_time": show.show_time,
        "price": show.price,
        "available_seats": available_seats
    }
    
    result = await shows_collection.insert_one(show_doc)
    return {"message": "Show created", "id": str(result.inserted_id)}

# View all bookings
@router.get("/bookings")
async def get_all_bookings():
    bookings = []
    cursor = bookings_collection.find()
    async for booking in cursor:
        # Get user details
        user = await users_collection.find_one({"_id": ObjectId(booking["user_id"])})
        
        booking_data = {
            "id": str(booking["_id"]),
            "user_email": user["email"] if user else "Unknown",
            "user_name": user["name"] if user else "Unknown",
            "show_id": booking["show_id"],
            "seats": booking["seats"],
            "total_price": booking["total_price"],
            "booking_date": booking["booking_date"],
            "status": booking["status"]
        }
        bookings.append(booking_data)
    
    return {"bookings": bookings}