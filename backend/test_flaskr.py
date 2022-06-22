import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://profesor:manasseh@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            "question":"test question",
            "answer":"test answer",
            "category":1,
            "difficulty":"5" 
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get test cases
    def test_get_questions(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories'])) 

    def test_404_request_beyond_valid_page(self):
        res = self.client().get('/api/v1.0/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    def test_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_405_if_method_not_allowed(self):
        res = self.client().post('/api/v1.0/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_category_questions(self):
        res = self.client().get('/api/v1.0/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_if_category_does_not_exist(self):
        res = self.client().get('/api/v1.0/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

#   post data

    def test_get_quizzes(self):
        res = self.client().post('/api/v1.0/quizzes', json={"quiz_category":{"id":1, "type":"Science"}, "previous_questions":[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_if_quiz_not_gotten(self):
        res = self.client().post('/api/v1.0/quizzes', json={"quiz_category":"1", "previous_questions":[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'your request is unprocessable')

    def test_create_question(self):
        res = self.client().post('/api/v1.0/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/api/v1.0/questions/15', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_questions_with_results(self):
        res = self.client().post('/api/v1.0/questions/search', json={"searchTerm":"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category']['id'], 1)

    def test_search_question_without_results(self):
        res = self.client().post('/api/v1.0/questions/search', json={"searchTerm":"gvjhcu"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)

    #    delete testcases

    def test_delete_question(self):
        res = self.client().delete('/api/v1.0/questions/24')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 24).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/api/v1.0/questions/24')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'your request is unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()