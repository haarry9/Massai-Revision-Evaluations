from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from bson import ObjectId
from datetime import datetime
from models.booking import BookingCreate, Booking
from models.movie import Movie
from models.theatre import Show
from database import (
    movies_collection, shows_collection,
    bookings_collection, users_collection,
    screens_collection, theatres_collection
)
from utils.auth import get_current_user, TokenData
from utils.email import send_booking_confirmation_email

router = APIRouter(tags=["User"], dependencies=[Depends(get_current_user)])

# Get all movies
@router.get("/movies")
async def get_movies():
    movies = []
    cursor = movies_collection.find()
    async for movie in cursor:
        movie_data = {
            "id": str(movie["_id"]),
            "title": movie["title"],
            "description": movie["description"],
            "duration_minutes": movie["duration_minutes"],
            "genre": movie["genre"],
            "language": movie["language"],
            "release_date": movie["release_date"]
        }
        movies.append(movie_data)
    return {"movies": movies}

# Get all shows
@router.get("/shows")
async def get_shows():
    shows = []
    cursor = shows_collection.find()
    async for show in cursor:
        # Get movie details
        movie = await movies_collection.find_one({"_id": ObjectId(show["movie_id"])})
        
        # Get screen details
        screen = await screens_collection.find_one({"_id": ObjectId(show["screen_id"])})
        
        # Get theatre details
        theatre = None
        if screen:
            theatre = await theatres_collection.find_one({"_id": ObjectId(screen["theatre_id"])})
        
        show_data = {
            "id": str(show["_id"]),
            "movie_title": movie["title"] if movie else "Unknown",
            "theatre_name": theatre["name"] if theatre else "Unknown",
            "screen_name": screen["name"] if screen else "Unknown",
            "show_date": show["show_date"],
            "show_time": show["show_time"],
            "price": show["price"]
        }
        shows.append(show_data)
    
    return {"shows": shows}

# Get show details with seat layout
@router.get("/shows/{show_id}")
async def get_show_details(show_id: str):
    if not ObjectId.is_valid(show_id):
        raise HTTPException(status_code=400, detail="Invalid show ID")
    
    show = await shows_collection.find_one({"_id": ObjectId(show_id)})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    # Get movie details
    movie = await movies_collection.find_one({"_id": ObjectId(show["movie_id"])})
    
    # Get screen details
    screen = await screens_collection.find_one({"_id": ObjectId(show["screen_id"])})
    
    # Get theatre details
    theatre = None
    if screen:
        theatre = await theatres_collection.find_one({"_id": ObjectId(screen["theatre_id"])})
    
    return {
        "id": str(show["_id"]),
        "movie": {
            "id": str(movie["_id"]),
            "title": movie["title"],
            "description": movie["description"],
            "duration_minutes": movie["duration_minutes"],
            "genre": movie["genre"],
            "language": movie["language"]
        } if movie else None,
        "theatre": {
            "name": theatre["name"],
            "location": theatre["location"]
        } if theatre else None,
        "screen": {
            "name": screen["name"],
            "total_seats": screen.get("seats", [])
        } if screen else None,
        "show_date": show["show_date"],
        "show_time": show["show_time"],
        "price": show["price"],
        "available_seats": show["available_seats"]
    }

# Get seat availability for a show
@router.get("/shows/{show_id}/seats")
async def get_seat_availability(show_id: str):
    if not ObjectId.is_valid(show_id):
        raise HTTPException(status_code=400, detail="Invalid show ID")
    
    show = await shows_collection.find_one({"_id": ObjectId(show_id)})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    return {
        "show_id": show_id,
        "available_seats": show["available_seats"]
    }

# Book tickets
@router.post("/bookings", status_code=status.HTTP_201_CREATED)
async def book_tickets(
    booking: BookingCreate,
    background_tasks: BackgroundTasks,
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(booking.show_id):
        raise HTTPException(status_code=400, detail="Invalid show ID")
    
    # Get show details
    show = await shows_collection.find_one({"_id": ObjectId(booking.show_id)})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    # Check if all requested seats are available
    available_seats = show["available_seats"]
    for seat in booking.seats:
        if seat not in available_seats:
            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat} is not available"
            )
    
    # Calculate total price
    total_price = show["price"] * len(booking.seats)
    
    # Get user details
    user = await users_collection.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create booking
    booking_doc = {
        "user_id": str(user["_id"]),
        "show_id": booking.show_id,
        "seats": booking.seats,
        "total_price": total_price,
        "booking_date": datetime.utcnow().isoformat(),
        "status": "confirmed"
    }
    
    result = await bookings_collection.insert_one(booking_doc)
    
    # Remove booked seats from available seats
    new_available_seats = [s for s in available_seats if s not in booking.seats]
    await shows_collection.update_one(
        {"_id": ObjectId(booking.show_id)},
        {"$set": {"available_seats": new_available_seats}}
    )
    
    # Send confirmation email in background
    booking_details = {
        "booking_id": str(result.inserted_id),
        "seats": booking.seats,
        "total_price": total_price
    }
    background_tasks.add_task(
        send_booking_confirmation_email,
        current_user.email,
        booking_details
    )
    
    return {
        "message": "Booking successful",
        "booking_id": str(result.inserted_id),
        "total_price": total_price
    }

# Get user's booking history
@router.get("/bookings")
async def get_bookings(current_user: TokenData = Depends(get_current_user)):
    # Get user
    user = await users_collection.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    bookings = []
    cursor = bookings_collection.find({"user_id": str(user["_id"])})
    
    async for booking in cursor:
        # Get show details
        show = await shows_collection.find_one({"_id": ObjectId(booking["show_id"])})
        
        movie = None
        screen = None
        theatre = None
        
        if show:
            movie = await movies_collection.find_one({"_id": ObjectId(show["movie_id"])})
            screen = await screens_collection.find_one({"_id": ObjectId(show["screen_id"])})
            if screen:
                theatre = await theatres_collection.find_one({"_id": ObjectId(screen["theatre_id"])})
        
        booking_data = {
            "id": str(booking["_id"]),
            "movie_title": movie["title"] if movie else "Unknown",
            "theatre_name": theatre["name"] if theatre else "Unknown",
            "screen_name": screen["name"] if screen else "Unknown",
            "show_date": show["show_date"] if show else "Unknown",
            "show_time": show["show_time"] if show else "Unknown",
            "seats": booking["seats"],
            "total_price": booking["total_price"],
            "booking_date": booking["booking_date"],
            "status": booking["status"]
        }
        bookings.append(booking_data)
    
    return {"bookings": bookings}

# Cancel booking
@router.delete("/bookings/{booking_id}")
async def cancel_booking(
    booking_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")
    
    # Get user
    user = await users_collection.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get booking
    booking = await bookings_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check if booking belongs to user
    if booking["user_id"] != str(user["_id"]):
        raise HTTPException(
            status_code=403,
            detail="You can only cancel your own bookings"
        )
    
    # Check if already cancelled
    if booking["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")
    
    # Update booking status
    await bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled"}}
    )
    
    # Add seats back to available seats
    show = await shows_collection.find_one({"_id": ObjectId(booking["show_id"])})
    if show:
        current_available = show["available_seats"]
        updated_available = current_available + booking["seats"]
        await shows_collection.update_one(
            {"_id": ObjectId(booking["show_id"])},
            {"$set": {"available_seats": updated_available}}
        )
    
    return {"message": "Booking cancelled successfully"}