import datetime as dt

from typing import Optional
from pydantic import BaseModel, Field

__all__ = ("ChapterInfo", "Course")

class ChapterInfo(BaseModel):
    chapter_id: int = Field(
        description="Id of the Chapter"
    )
    
    name: str = Field(
        description="Name of the Chapter"
        )

    text: Optional[str] = Field(
        description="About of the Chapter"
        )
    
    rating: Optional[float] = Field(alias="rating", description="Rating of the Chapter")
    
    no_of_ratings: Optional[int] = Field(alias="no_of_ratings", description="Number of Ratings of the Chapter")



class Course(BaseModel):
    course_id: int = Field(description="Id of the Course")
    
    name: str = Field(alias="name", default=None, description="Name of the Course")
    
    description: Optional[str] = Field(alias="description", description="Description of the Course")

    date: dt.datetime = Field(alias="date", description="Date of the Course Creation")

    domain: list[str] = Field(alias="domain", description="Domain related to the Course")

    chapters: Optional[list[ChapterInfo]] = Field(alias="chapters", description="List of Chapters of the Course")
    
    rating: Optional[float] = Field(alias="rating", description="Rating of the Course")
    
    no_of_ratings: Optional[int] = Field(alias="no_of_ratings", description="Number of Ratings of the Course")

class RateResponse(BaseModel):
    message: str