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
        self.username = 'postgres'
        self.password = 'abodov1281'
        self.ip_port = 'localhost:5432'

        self.database_path = "postgres://{}:{}@{}/{}".format(self.username, self.password, self.ip_port,
                                                             self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_get_gategories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalCategories'])
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_default(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertFalse(data['currentCategory'])

    def test_get_paginated_questions_page_1(self):
        res = self.client().get('/api/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertFalse(data['currentCategory'])

    def test_404_get_paginated_questions_invalid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # def test_delete_question(self):
    #     res = self.client().get('/api/questions')
    #     data = json.loads(res.data)
    #     len_before = data['totalQuestions']
    #
    #     delete_id = 15
    #     res = self.client().delete('/api/questions/'+str(delete_id))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], str(delete_id))
    #     self.assertTrue(str(delete_id) not in data['questions'])
    #     self.assertTrue(delete_id not in data['questions'])
    #
    #     res = self.client().get('/api/questions')
    #     data = json.loads(res.data)
    #     len_after = data['totalQuestions']
    #
    #     self.assertTrue(len_before ==  len_after + 1)

    def test_404_delete(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_before = data['totalQuestions']

        delete_id = 100000
        res = self.client().delete('/api/questions/' + str(delete_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_after = data['totalQuestions']

        self.assertTrue(len_before == len_after)

    def test_200_add_question(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_before = data['totalQuestions']

        question = {'question': 'Test', 'answer': 'this is a test', 'difficulty': '4', 'category': '4'}

        res = self.client().post('/api/questions', json = question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_after = data['totalQuestions']

        self.assertTrue(len_before == len_after - 1)

    def test_422_add_question(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_before = data['totalQuestions']

        question = {'question!': 'Test', 'answer': 'this is a test', 'difficulty': '4', 'category': '4'}

        res = self.client().post('/api/questions', json = question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        len_after = data['totalQuestions']

        self.assertTrue(len_before == len_after)


    def test_200_search(self):
        res = self.client().post('/api/questions/search', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertFalse(data['currentCategory'])

    def test_422_wrong_input_seach(self):
        res = self.client().post('/api/questions/search', json={'search': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_no_input_seach(self):
        res = self.client().post('/api/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_category_questions(self):
        category_id = 1  # Science
        res = self.client().get('/api/categories/' + str(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_422_invalid_input(self):
        res = self.client().get('/api/categories/' + "aaaaaaaaa")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_404_no_category(self):

        category_id = 11  # Science
        res = self.client().get('/api/categories/' + str(category_id))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_200_quiz_with_category(self):
        quiz_category = {'type': 'History', 'id': '4'}
        previous_questions = [5, 9]

        res = self.client().post('/api/quizzes', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_200_quiz_without_category(self):
        quiz_category = {'type': None, 'id': None}
        previous_questions = [5, 9]

        res = self.client().post('/api/quizzes', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_quiz_with_wrong_category(self):
        quiz_category = {'type': 'Something', 'id': '11'}
        previous_questions = []

        res = self.client().post('/api/quizzes', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not Found')

    def test_422_quiz(self):
        quiz_category = {'error': 'this should cause an error'}
        previous_questions = [5, 9]

        res = self.client().post('/api/quizzes', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
