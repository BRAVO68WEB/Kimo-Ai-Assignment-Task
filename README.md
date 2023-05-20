## API Project Readme

This is a Python API project for managing trades using FastAPI framework and MongoDB database. This project is created for the backend developer position.

### Requirements

- Python 3.6 or above
- MongoDB
- fastapi
- pymongo
- python-dotenv

### Installation

1. Clone the repository:

```
git clone https://github.com/BRAVO68WEB/Kimo-Ai-Assignment-Task.git
cd Kimo-Ai-Assignment-Task
```

2. Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create a .env file and set the MONGO_URI variable to your MongoDB URI:

```
MONGO_URI=<your-mongodb-uri>
```

### Usage

- Start the API server:

```
uvicorn main:app --reload
```

- Open your web browser and go to http://localhost:8000/docs to view the Swagger UI for the API.

- Use the Swagger UI to test the API endpoints.

### Tests

- Run the tests:

```
pytest
```