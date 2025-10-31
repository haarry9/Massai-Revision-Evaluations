import asyncio

async def send_booking_confirmation_email(email: str, booking_details: dict):
    await asyncio.sleep(1)
    print(f"Email sent to {email}")
    print(f"Booking Details: {booking_details}")