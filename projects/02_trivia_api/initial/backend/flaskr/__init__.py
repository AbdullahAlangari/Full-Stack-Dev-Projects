import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db
from sqlalchemy import func


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @cross_origin
    @app.route('/api/categories', methods=["GET"])
    def get_categories():
        categories = get_category_dict()
        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories,
            'totalCategories': len(categories)
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @cross_origin
    @app.route('/api/questions', methods=["GET"])
    def get_questions():
        db_questions = Question.query.all()
        paginated_questions = paginate_questions(request, db_questions)
        category_dict = get_category_dict()

        if len(paginated_questions) == 0 or len(category_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'totalQuestions': len(db_questions),
            'categories': category_dict,
            'currentCategory': None
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    # The 422 error is left there for when something is entered incorrectly to the db
    @cross_origin
    @app.route('/api/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        error = False
        if question is None:
            abort(404)
        try:
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if error:
            abort(422)
        db_questions = Question.query.all()
        current_questions = [question.id for question in db_questions]

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_books': len(Question.query.all())
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @cross_origin
    @app.route('/api/questions', methods=['POST'])
    def add_question():

        error = True

        try:
            data = request.get_json()
            print(data)
            question = Question(
                question=data['question'],
                answer=data['answer'],
                difficulty=data['difficulty'],
                category=data['category']
            )
            db.session.add(question)
            db.session.commit()
            error = False
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(422)

        return jsonify({
            'success': True
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    # allowed for users to receive no results if nothing exists their search entry (NOT 404)
    @cross_origin
    @app.route('/api/questions/search', methods=['POST'])
    def question_search():

        try:
            data = request.get_json()
            db_search = Question.query.filter(
                func.lower(Question.question).contains(func.lower(data['searchTerm']))).all()
            paginated_results = paginate_questions(request, db_search)
        except:
            abort(422)

        return jsonify({
            'questions': paginated_results,
            'totalQuestions': len(db_search),
            'currentCategory': None,
            'success': True
        })

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    # Intentionally allowed users to retreive categories with no questions (NO ERROR)
    @cross_origin
    @app.route('/api/categories/<category_id>', methods=['GET'])
    def get_category_questions(category_id):
        try:
            db_questions = Question.query.filter_by(category=category_id).all()
            db_category = Category.query.get(category_id)
        except:
            abort(422)
        if db_category is None:
            abort(404)

        formatted_questions = [question.format() for question in db_questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions),
            'currentCategory': db_category.type
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @cross_origin
    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():

        data = request.get_json()
        print(data)
        try:
            previous_questions = data['previous_questions']
            category_id = data['quiz_category']['id']
        except:
            abort(422)
        if category_id is not None:
            db_questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()

        else:
            db_questions = Question.query.all()
        if len(db_questions) == 0:
            abort(404)
        quiz_questions = []

        formatted_questions = [question.format() for question in db_questions]
        if formatted_questions == 0:
            abort(500)
        for question in formatted_questions:

            if question['id'] not in previous_questions:
                quiz_questions.append(question)
        if quiz_questions:
            quiz_question = random.choice(quiz_questions)
        else:
            quiz_question = None

        return jsonify({
            'success': True,
            'question': quiz_question
        })

    '''
  HELPER FUNCTIONS
  '''

    def paginate_questions(request, db_questions):

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        page_questions = db_questions[start:end]
        formatted_questions = [question.format() for question in page_questions]
        return formatted_questions

    def get_category_dict():
        db_categories = Category.query.order_by(Category.id).all()
        # formatted_categories = [category.format() for category in db_categories]

        category_dict = {}
        for category in db_categories:
            category_dict[category.id] = category.type
        return category_dict

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 405,
            'message': 'Method Not Allowed, Look up the documentation'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 500,
            'message': 'There is a bug in the system, sorry about that :< Please report the error at '
                       'help@trivia.legit.com '
        }), 500

    return app
