# Full Stack API Final Project


## Full Stack Trivia

This project is a trivia game for anyone that wishes to participate :> It gives you the option to add and remove questions from specific categories, play the game with one category or all categories, and getting questions related to a specific category. This is the second project in Udacity's Full Stack Web Development Nanodegree: Course 2: API Development and Documentation.

The Application allows the user to:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


all backend code follow [PEP8 Style guidelines](https://www.python.org/dev/peps/pep-0008/)

## Getting started
Fork this project repository or download zip, then run the code in your favourite text editor (notes that this project uses Python3-Flask for backend and ReactJS for frontend)

### Prerequisites
Developers using this project shoudl already have Python3, pip3, and node installed in their local machines

### Backend
Navigate to the backend folder and run <pip3 install requirements.txt>, which includes all required packages

  
  
To run the backend the first time run the following commands
  <export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask run>

These command put the application in development and directs our application to use the <__init__.py> file in our flaskr folder, and runs flask in development mode which makes it so much easier to debug and test code by restarting the server whenever any chnages occur to the code, but remember to change the <FLASK_ENV> to production mode when the application is put to production

    
    
After the initial setup, it is sufficient to run
    <flask run>


The application is run on localhost on <https://127.0.0.1:5000/> or <localhost:5000/>, which is a proxy in the frontend.

### Frontend

  To run the frontend the first time, navigate to the frontend folder and run the following commands
  <npm install
   npm start>
    
    
After the initial setup, it is sufficient to run
    <npm start>

By default, the frontend will run on <localhost:3001>      


##Tests
In order to run tests navigate to the backend folder and run the following commands:

<dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py>
      
The first time you run the tests, omit the dropdb command.

All tests are kept in <test_flaskr.py> and should be maintained and run as updates are made to app functionality.
      
##API References
      
##Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
      
Authentication: This version of the application does not require authentication or API keys.
###Error Handling
      
Errors are returned as JSON objects in the following format:
{
    "success": False, 
    "error": 404,
    "message": "Not Found"
}
The API will return three error types when requests fail:

404: Not Found
405: Method Not Allowed, Look up the documentation
422: unprocessable
500: There is a bug in the system, sorry about that :< Please report the error at help@trivia.legit.com
                                                             
###End Points

#### GET /api/categories
* General
  Returns a list of category objects, success value, and total number of cateogories.
                                                             
                                                             
* Sample: curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "totalCategories": 6
}

                                                             
#### GET /questions
* General:
                                                             
Returns a list of question objects, category objects, current category (if applicable), success value, and total number of questions.
                                                             
Results are paginated in groups of 10. Request arguement can request specific pages, or be left empty for a default of page 1


                                                           
* Sample: curl http://127.0.0.1:5000/api/questions
                                                             
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
(venv) klorex@DESKTOP-FUB9S81:~/full_stack_web/demos/FSND/projects/02_trivia_api/initial/backend$ curl localhost:5000/api/questions
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}

#### DELETE /questions/{question_id}
* General:
                                                             
Returns a the deleted question id, the current list of question ids, the total number of questions, and the success value.
                                                             
* Sample: curl -X DELETE localhost:5000/api/questions/11

                                                             
{
  "deleted": "11",
  "questions": [
    9,
    2,
    4,
    6,
    10,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    25,
    26,
    27,
    28
  ],
  "success": true,
  "total_questions": 21
}


         
#### POST /api/questions
* General:
                                                             
Returns success value of POST request.
                                                             
* Sample: curl -X POST -H "Content-Type: application/json" -d '{"question": "This is
 a qusestion of your choice","answer": "The corerct answer", "difficulty":"4", "catego
ry":"5"}' http://127.0.0.1:5000/api/questions
                                                             
                                                             
{
  "success": true
}
 
#### POST /api/questions/search
* General:
                                                             
Returns list of resulting question objects, a null currentCategory, success value and total number of questions.
                                                             
* Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}
' http://127.0.0.1:5000/api/questions/search
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in
 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the
role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about
 a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
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
  "totalQuestions": 8
}
                                                             
#### GET /api/categories/{category_id}
                                                             
* General:
Returns list of resulting question objects, the type of the urrent category, success value and total number of questions.
                                                             
* Sample: curl localhost:5000/api/categories/2
{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optic
al illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and
a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}

                                                             

#### POST /api/questions/search
* General:
                                                             
Returns list of resulting question objects, a null currentCategory, success value and total number of questions.
                                                             
* Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}
' http://127.0.0.1:5000/api/questions/search
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in
 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the
role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about
 a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
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
  "totalQuestions": 8
}
                                                             
#### POST /api/quizzes
                                                             
* General:
Returns a question which has not been previously asked by checking an input <previous_Questions> and an optional quiz category 
                                                             
* Sample: <curl -X POST -H "Content-Type: application/json" -d '{"previous_questions" : [5,9], "quiz_category" : {"id":null, "type":null}}' http://127.0.0.1:5000/api/quizze
s>
{
  "question": {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}

