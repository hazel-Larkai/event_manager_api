from fastapi import APIRouter, Form, HTTPException, status
from typing import Annotated
from pydantic import EmailStr
from db import users_collection
import bcrypt

# Create Users router
users_router = APIRouter()

# Define endpoints
@users_router.post("/users/register")
def register_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)]
):
    # Ensure user does not already exists
    user_count = users_collection.count_documents(filter={"email": email})
    if user_count > 0:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists!") 
    # Hash user password
    hashed_password = bcrypt.hashpw(bytes(password), bcrypt.gensalt())

    # Save user into database
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": password
    })

    # Return responmse
    return {"message" : f"User {username} registered sucessfully!"}