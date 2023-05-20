from enum import Enum
from fastapi import FastAPI
import datetime as dt
from datetime import timezone

from models.operations import CourseRead
from database import collection
from models.schemas import RateResponse, Course, ChapterInfo

class SortOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'

class SortBy(str, Enum):
    course_id = 'course_id'
    name = 'name'
    description = 'description'
    date = 'date'
    rating = 'rating'

class DomainList(str, Enum):
    computer_vision = 'computer vision'
    artificial_intelligence = 'artificial intelligence'
    mathematics = 'mathematics'
    programming = 'programming'
    
class RateValue(str, Enum):
    very_bad = 1
    bad = 2
    nornal = 3
    good = 4
    very_good = 5

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/courses")
def show(
    page_no: int = 0,
    per_page: int = 10,
    sort_by:SortBy = "course_id",
    sort_order: SortOrder = "desc",
    domain: DomainList = None,
    rate: RateValue = None
    ) -> list[Course]:
    
    query = {}
    
    if(domain):
        query["domain"] = domain
        
    if(rate):
        query["rating"] = {"$gte": int(rate)}
    
    sort_dir = 1
    if(sort_order == 'asc'):
        sort_dir = 1
    else:
        sort_dir = -1

    cursor = collection.find(query, {'_id': 0, 'chapters': 0, 'description': 0}).limit(per_page).skip(page_no * per_page).sort(
        key_or_list=sort_by, direction=sort_dir)
    
    return [CourseRead(**document) for document in cursor]

@app.get("/course/{id}")
def get_by_id(id:int) -> Course:
    course = collection.find_one({"course_id": id,}, {'_id': 0})
    return CourseRead(**course)

@app.get("/course/{id}/{chapter}")
def get_chapter(id:int, chapter: int) -> ChapterInfo:
    course = collection.find_one({"course_id": id,}, {'_id': 0})
    chapters = course["chapters"]
    for ch in chapters:
        if(ch["chapter_id"] == chapter):
            return ch
    return {"message": "Chapter not found"}

@app.post("/course/{id}/rate")
def rate(id:int, rate: float) -> RateResponse:
    course = collection.find_one({"course_id": id}, {'_id': 0})
    no_of_ratings = course["no_of_ratings"]
    rating = course["rating"]
    new_rating = (rating * no_of_ratings + rate) / (no_of_ratings + 1)
    collection.update_one({"course_id": id}, {"$set": {"rating": new_rating, "no_of_ratings": no_of_ratings + 1}})
    return {"message": "Rated successfully"}

@app.post("/course/{id}/{chapter}/rate")
def rate_chapter(id:int, chapter: int, rate: float) -> RateResponse:
    course = collection.find_one({"course_id": id}, {'_id': 0})
    chapters = course["chapters"]
    for ch in chapters:
        if(ch["chapter_id"] == chapter):
            no_of_ratings = ch["no_of_ratings"]
            rating = ch["rating"]
            new_rating = (rating * no_of_ratings + rate) / (no_of_ratings + 1)
            collection.update_one({"course_id": id, "chapters.chapter_id": chapter}, {"$set": {"chapters.$.rating": new_rating, "chapters.$.no_of_ratings": no_of_ratings + 1}})
            return {"message": "Rated successfully"}
    return {"message": "Chapter not found"}