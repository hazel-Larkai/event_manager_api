from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from db import events_collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv
from routes.events import events_router
from routes.users import users_router

# Configure cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)



app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "You are on the home page"}


# Include routers
app.include_router(users_router)
app.include_router(events_router)