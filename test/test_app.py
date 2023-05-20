import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
import json
from models.operations import CourseRead
from database import collection
from models.schemas import RateResponse, Course, ChapterInfo

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example usage
file_path = 'data/db.json'

@pytest.fixture
def client():
    return TestClient(app)

def test_home_endpoint(client, mocker):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_health_endpoint(client, mocker):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
    
def test_show_courses_endpoint(client, mocker):
    response = client.get("/courses")
    assert response.status_code == 200
    resdata = response.json()
    cursor = collection.find({}, {'_id': 0, 'chapters': 0, 'description': 0}).sort(
        key_or_list="course_id", direction=-1)
    assert len(resdata) == 4
    assert resdata[0]["domain"] == cursor[0]["domain"]
    assert resdata[0]["rating"] == cursor[0]["rating"]
    assert resdata[0]["name"] == cursor[0]["name"]
    assert resdata[0]["course_id"] == cursor[0]["course_id"]
    assert resdata[0]["no_of_ratings"] == cursor[0]["no_of_ratings"]
    
def test_show_courses_endpoint(client, mocker):
    cursor = collection.find({}, {'_id': 0, 'chapters': 0, 'description': 0}).sort(
        key_or_list="course_id", direction=-1)
    print(str(cursor[0]["course_id"]))
    response = client.get("/course"+"/"+str(cursor[0]["course_id"]))
    assert response.status_code == 200
    resdata = response.json()
    assert resdata["domain"] == cursor[0]["domain"]
    assert resdata["rating"] == cursor[0]["rating"]
    assert resdata["name"] == cursor[0]["name"]
    assert resdata["course_id"] == cursor[0]["course_id"]
    assert resdata["no_of_ratings"] == cursor[0]["no_of_ratings"]
    
def test_show_chapter_endpoint(client, mocker):
    cursor = collection.find({}, {'_id': 0,'description': 0}).sort(
        key_or_list="course_id", direction=-1)
    print(str(cursor[0]["chapters"]))
    response = client.get("/course/"+str(cursor[0]["course_id"])+"/"+str(cursor[0]["chapters"][0]["chapter_id"]))
    assert response.status_code == 200
    resdata = response.json()
    assert resdata["name"] == cursor[0]["chapters"][0]["name"]
    assert resdata["chapter_id"] == cursor[0]["chapters"][0]["chapter_id"]
    assert resdata["rating"] == cursor[0]["chapters"][0]["rating"]
    assert resdata["no_of_ratings"] == cursor[0]["chapters"][0]["no_of_ratings"]
    
def test_rate_course_endpoint(client, mocker):
    cursor = collection.find({}, {'_id': 0, 'chapters': 0, 'description': 0}).sort(
        key_or_list="course_id", direction=-1)
    response = client.post("/course/"+str(cursor[0]["course_id"])+"/rate?rate=4.5")
    assert response.status_code == 200
    resdata = response.json()
    assert resdata["message"] == "Rated successfully"
    
def test_rate_chapter_endpoint(client, mocker):
    cursor = collection.find({}, {'_id': 0,'description': 0}).sort(
        key_or_list="course_id", direction=-1)
    response = client.post("/course/"+str(cursor[0]["course_id"])+"/"+str(cursor[0]["chapters"][0]["chapter_id"])+"/rate?rate=4.5")
    assert response.status_code == 200
    resdata = response.json()
    assert resdata["message"] == "Rated successfully"