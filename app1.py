from config import app, db
from flask import flash , Flask ,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, program




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




login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




def gettime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
    return formatted_datetime

@app.route("/forgotpass",methods=['GET','POST'])
def forgotpass():
    if request.method == 'POST':
        email = request.form['email']
        new_pass = request.form['new_pass']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password_hash=new_pass
            user.set_password(new_pass)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            flash('email dosent exist')
    return render_template('forgot.html')



# Update the routes to handle user authentication

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
                # Check if the email is already taken
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already taken. Please choose a different email.', 'error')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_required
@app.route("/home",methods=['GET','POST'])
def index():
    if request.method=='POST':

        question=request.form['question']
        solution=request.form['solution']
        if len(question)==0 or len(solution)==0:
            flash('empty question/Solution canot be uploaded')
            return redirect('/')  
        uuid = generator.generate_unique_id(current_user.username)  

        # info=todo(todo_task=todo_task,todo_desc=todo_desc,todo_pry=pry,date_created=gettime(),user_id=current_user.id)
        info = program(program_question=question,program_solution=solution,date_created=gettime(),user_id=current_user.id,program_id=uuid)
        db.session.add(info)
        # print(info)
        db.session.commit()
        return redirect('/')
  
    allinfo = program.query.all()
    return render_template('index copy.html',todos=allinfo,name=current_user.username, current_user_id = current_user.id)



@login_required
@app.route('/search', methods=['GET','POST'])
def search():
    query = request.args.get('query')
    if query:
        results = program.query.filter(program.program_id.ilike(f'%{query}%')).all()
        
    else:
        results = [] 

    return render_template('sr.html', query=query, results=results,name=current_user.username, current_user_id = current_user.id)



@login_required
@app.route("/Big_DRAGOON/update/<int:pk>",methods=['GET','POST'])
def update(pk):
    if request.method=='POST':

        todo_task=request.form['todo']
        todo_desc=request.form['desc']
        if len(todo_task)==0:
            flash('empty messages canot be sent')
            return redirect(f'/Big_DRAGOON/update/{pk}')

        infos=program.query.filter_by(id=pk).first()
        
        infos.program_question=todo_task
        infos.program_solution=todo_desc
        db.session.add(infos)
        db.session.commit()
        return redirect('/')
    allinfo = program.query.filter_by(id=pk).first()
    return render_template('update.html',todos=allinfo)








