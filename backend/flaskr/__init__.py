import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questiions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = [question.format() for question in selection]
    return current_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)#, resources={r"/api/v1.0/*":{"origins":"*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Header", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1.0/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.order_by(Category.id).all()

        if not categories:
            abort(404)

        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": formatted_categories 
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1.0/questions')
    def get_questions():
       
        current_category = Category.query.get(1)
        questions = Question.query.filter(Question.category==current_category.id).order_by(Question.id).all()
        current_questions = paginate_questiions(request, questions)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404) 

        return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions':len(current_questions),
                'categories': formatted_categories,
                'current_category': current_category.type
            })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
        except:
            abort(422)

        return jsonify({
            "success":True
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_question():
        req = request.get_json()

        if not req:
            abort(400)

        try:

            #get the values
            question = req.get('question', None) 
            answer = req.get('answer', None) 
            category = req.get('category', None) 
            difficulty_score = req.get('difficulty', None) 
           
            #save into the database
            new_question = Question(question=question, answer=answer, category=category, difficulty=int(difficulty_score))
            new_question.insert()

        except Exception as e:
            print(e)
            abort(422)

        return jsonify({
            'success':True
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1.0/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm')

        search_results = Question.query.filter(Question.question.ilike('%'+ search_term + '%')).order_by(Question.id).all()
        results = [result.format() for result in search_results]
        current_category = Category.query.get(1)
        
        return jsonify({
            'success':True,
            'questions': results,
            'total_questions': len(results),
            'current_category': current_category.format()
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1.0/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        try:
            category = Category.query.get(cat_id)
            cat_questions = Question.query.order_by(Question.id).filter(Question.category == category.id).all()
            current_questions = [question.format() for question in cat_questions]
    
        except:
            abort(404)
        

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(cat_questions),
            "current_category": category.format()
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_quizz():
        try:
            req = request.get_json()
            
            if not req:
                abort(400)

            data = {**req}
            category_id = data.get('quiz_category', None)
            
            previous_questions = data.get('previous_questions', [])
            
            if category_id['id'] == 0:
            
                questions = Question.query.order_by(Question.id.desc()).all()
                
            else:    
                category = Category.query.get(category_id['id'])

                questions = Question.query.order_by(Question.id.desc()).filter(Question.category==category.id).all()

            last_question_id = questions[0].id
            first_question_id = questions[-1].id

            #implement checking through the id'ss

            questions_id = [question.id for question in questions]

            questions_count = len(questions)
            pick = random.randrange(first_question_id, last_question_id + 1)
            
            if len(previous_questions) < questions_count:
                while pick:
                    if (pick not in previous_questions) and (pick in questions_id):
                        break
                    else:
                        pick = random.randrange(first_question_id, last_question_id + 1)

                previous_questions += [pick]
                current_question = Question.query.get(pick)
                
            else:
                return jsonify({
                    'success':True
                })

            return jsonify(
                {
                    'success': True,
                    'question': current_question.format()
                }
            )
        except:
            abort(422)
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def request_not_found(error):
        return jsonify({
            'success': False,
            'message': "resource not found",
            'error': 404
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'error': 400,
            'message': 'bad request'
        }) , 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message':'your request is unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message':'method not allowed'
        }), 405
    return app

