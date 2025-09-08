from fastapi import FastAPI, Form, File, UploadFile
from db import events_collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated


class EventModel(BaseModel):
    title: str
    description: str


app = FastAPI()


@app.get("/")
def get_home():
    return {"message": "You are on the home page"}


# Events endpoints
@app.get("/events")
def get_events(title="", description="", limit=10, skip=0):
    # Get all events from database
    events = events_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()
    # Return response
    return {"data": list(map(replace_mongo_id, events))}


@app.post("/events")
def post_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
):
    # Insert event into database
    # events_collection.insert_one(event.model_dump())
    # Return response
    return {"message": "Event added sucessfully"}


@app.get("/events/{event_id}")
def get_event_by_id(event_id):
    # Get event from database by id
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # Return response
    return {"data": replace_mongo_id(event_id)}
