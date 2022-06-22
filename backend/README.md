# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API REFERENCE

### GETTING STARTED
- BASE URL: At present this app can only be run locally and not hosted as a base URL. The backend app is
hosted at the default, `http://localhost:5000/`, which is set as a proxy in the frontend configuration.
- AUTHENTICATION: This version of the application does not use authentication or API keys

### ERROR HANDLING 
Errors are returned as JSON objects in the following format:

```
{
    "success":False,
    "error":400,
    "message":"bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Allowed

### ENDPOINTS
#### GET  /api/v1.0/questions
- General:
    - Returns a list of question objects, a list categories object, success value, current category, and total number of current questions 
    - The question object are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Request Arguments: None
- Sample: `curl http:localhost:5000/api/v1.0/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```

#### GET /api/v1.0/categories
- General:
    - Returns a list of category objects and a success value.
    - Request Arguments: None
- Sample: `curl http://localhost:5000/api/v1.0/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```
#### GET /api/v1.0/categories/{category_id}/questions
- General:
    - Returns a list of question objects that belong to the specified category, success value, number of questions returned, and the category specified in the url.
    - Request Arguments: None
- Sample: `curl http://localhost:5000/api/v1.0/categories/1/questions`

```
{
  "current_category": {
    "id": 1,
    "type": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```

#### POST /api/v1.0/questions
- General:
    - Creates a question object by using the question, answer, category and difficulty fields passed from the frontend
    - Returns a success value
    - Request Arguments: question, answer, category and difficulty
- Sample: `curl http://localhost:5000/api/v1.0/questions -X POST -H "Content-Type:application/json" -d '{"question":"test question", "answer":"test answer", "category":1, "difficulty":"5" }'`

```
{
  "success": true
}

```
#### POST /api/v1.0/questions/search
- General:
    - Searches all the questions in the database and Return questions which matches the searchTerm being passed from the frontend, success value, number of questions returned and current category.
    - Request Arguments: searchTerm 
- Sample: `curl http://localhost:5000/api/v1.0/questions/search -X POST -H "Content-Type:application/json" -d '{"searchTerm":"title"}'`

```
{
  "current_category": {
    "id": 1,
    "type": "Science"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```

#### POST /api/v1.0/quizzes
- General:
    - Returns a random questions within the given category, if provided, and that is not one of the previous questions.
    - Request Arguments: quiz_category and previous_question
-Sample: `curl http://localhost:5000/api/v1.0/quizzes -X POST -H "Content-Type:application/json" -d '{"quiz_category":{"id":1,"type":"Science"}, "previous_questions":[]}'`

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}

```

#### DELETE /api/v1.0/questions/{question_id}
- General:
    - Deletes the question of the given id in the request if it exists.
    - Returns a success value
    - Request Arguments: None
- Sample: `curl http://localhost:5000/api/v1.0/questions/29 -X DELETE`

```
{
  "success": true
}

```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
