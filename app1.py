from config import app, db
from flask import flash , Flask ,render_template,redirect,request,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, program
from flask_caching import Cache
cache = Cache(app)
from sqlalchemy import desc



import random
import string


class UniqueIDGenerator:
    def __init__(self):
        self.id_count = {}

    def generate_unique_id(self, name):
        # Initialize count for name if it doesn't exist
        if name not in self.id_count:
            self.id_count[name] = 1
        else:
            self.id_count[name] += 1

        # Generate random length for numbers and alphabets
        max_length = min(12 - len(name), 12)
        num_length = random.randint(1, max_length // 2)
        alpha_length = max_length - num_length

        # Generate random numbers with specified length
        random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(num_length)])

        # Generate random alphabets with specified length
        random_alphabets = ''.join(random.choices(string.ascii_lowercase, k=alpha_length))

        # Generate unique ID
        unique_id = f"{name}_{random_numbers}{random_alphabets}"

        return unique_id

# Example usage
generator = UniqueIDGenerator()
# print(generator.generate_unique_id("John"))  # Output: John_83xq





def gettime():
    current_datetime = datetime.now()  # Get current UTC time
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Format to 'YYYY-MM-DD HH:MM:SS'
    return formatted_datetime


# Endpoint to get all programs, ordered by date_created in descending order
@app.route("/v1/c", methods=['GET'])
@cache.cached(timeout=300, key_prefix="all_code")
def get():
    allinfo = program.query.order_by(desc(program.date_created)).all()
    data = [{'question': i.program_question, 'solution': i.program_solution, 'date': i.date_created, 'id': i.id,'language':i.program_language } for i in allinfo]
    for i in allinfo:
        print(i.program_language,i.id)
    return jsonify(data), 200

# Endpoint to get a specific program by ID
@app.route("/v1/c/<int:id>", methods=['GET'])
def get_id(id):
    print("accessing..")
    program_info = program.query.filter_by(id=id).first()
    if program_info:
        return jsonify({
            'question': program_info.program_question,
            'solution': program_info.program_solution,
            'date': program_info.date_created,
            'id': program_info.id,
            'language': program_info.program_language
        }), 200
    else:
        return jsonify({'msg': 'Program not found'}), 404

# Endpoint to upload a new program
@app.route("/v1/upload", methods=['POST'])
def post():
    question = request.json.get('question')
    solution = request.json.get('solution')
    language = request.json.get('language')

    if not question or not solution or not language:
        return jsonify({'msg': 'Empty question/solution cannot be uploaded'}), 401
    print(question,solution,language)
    new_program = program(
        program_question=question,
        program_solution=solution,
        date_created=gettime(),
        user_id=12,
        program_language=language
    )

    try:
        db.session.add(new_program)
        db.session.commit()
        cache.delete("all_code")  # Invalidate the cache to reflect new data
        return jsonify({'msg': 'Success'}), 200
    except Exception as e:
        return jsonify({'msg': 'Failed to upload program'}), 500
    
@app.route("/v1/delete/<int:id>", methods=['DELETE'])
def delete_route(id):
    program_info = program.query.filter_by(id=id).first()
    if program_info:
        db.session.delete(program_info)
        db.session.commit()
        cache.delete("all_code")
        return jsonify({'msg': 'Program deleted successfully'}), 200
    return jsonify({'msg': 'Program not found'}), 404

@app.route("/v1/update/<int:id>", methods=['PUT'])
def edit(id):
    program_info = program.query.filter_by(id=id).first()
    if program_info:
        question = request.json.get('question')
        solution = request.json.get('solution')
        language = request.json.get('language')
        if not question or not solution or not language:
            return jsonify({'msg': 'Empty question/solution cannot be uploaded'}), 401

        program_info.program_question = question
        program_info.program_solution = solution
        program_info.program_language = language
        try:
            db.session.commit()
            cache.delete("all_code")
            return jsonify({'msg': 'Program updated successfully'}), 200
        except Exception as e:
            return jsonify({'msg': 'Failed to update program'}), 500

