from flask import flash , Flask ,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///active_database.db"

# app.config['SQLALCHEMY_DATABASE_URI']="postgresql://fl0user:vg2txbzP8wYA@ep-white-sun-a11thfri.ap-southeast-1.aws.neon.fl0.io:5432/database"
# app.config['SQLALCHEMY_DATABASE_URI']="postgresql://fl0user:sE3atNvoL4bu@ep-soft-boat-a1mzgth3.ap-southeast-1.aws.neon.fl0.io:5432/database?sslmode=require"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://r.tarunnayaka25042005:NI9Odhun6xWG@ep-delicate-resonance-a1afqwgy.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"


app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']= False
app.secret_key = "secreate_key"
app.config['UPLOADED_PHOTOS_DEST']='static'
db = SQLAlchemy(app)

# Priority and Categorization: Enable
# users to prioritize tasks and assign
# categories. Implement a system for
# organizing tasks based on urgency or
# importance.

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    todos = db.relationship('todo', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todo_task = db.Column(db.String(500),nullable=False )
    todo_desc = db.Column(db.String(500),nullable=False )
    todo_status = db.Column(db.Boolean,nullable=False ,default=False)  
    todo_pry = db.Column(db.Boolean,nullable=False ,default=False)  
    date_created = db.Column(db.String(300), default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"status {self.todo_status} - task {self.todo_task}- "

    

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
        return redirect(url_for('index'))
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

        todo_task=request.form['todo']
        todo_desc=request.form['desc']
        pry = request.form['pry']
        # print(pry)
        if len(todo_task)==0:
            flash('empty messages canot be sent')
            return redirect('/')    
        if pry=='high':
            pry=True
        else:
            pry=False

        info=todo(todo_task=todo_task,todo_desc=todo_desc,todo_pry=pry,date_created=gettime(),user_id=current_user.id)
        db.session.add(info)
        # print(info)
        db.session.commit()
        return redirect('/')
  
    allinfo = todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html',todos=allinfo,name=current_user.username)


@login_required
@app.route("/todo/change/<int:id>")
def change(id):
    info=todo.query.filter_by(id=id).first()
    if info.todo_pry==True:
        info.todo_pry=False
    else:
        info.todo_pry=True
    db.session.add(info)
    db.session.commit()
    return redirect('/')

@login_required
@app.route("/todo/changesr/<int:id>")
def changesr(id):
    info=todo.query.filter_by(id=id).first()
    if info.todo_pry==True:
        info.todo_pry=False
    else:
        info.todo_pry=True
    db.session.add(info)
    db.session.commit()
    return redirect('/')


@login_required
@app.route("/todo/update/<int:pk>",methods=['GET','POST'])
def update(pk):
    if request.method=='POST':

        todo_task=request.form['todo']
        todo_desc=request.form['desc']
        if len(todo_task)==0:
            flash('empty messages canot be sent')
            return redirect(f'/todo/update/{pk}')

        infos=todo.query.filter_by(id=pk).first()
        
        infos.todo_task=todo_task
        infos.todo_desc=todo_desc
        db.session.add(infos)
        db.session.commit()
        return redirect('/')
    allinfo = todo.query.filter_by(id=pk).first()
    return render_template('update.html',todos=allinfo)


@login_required
@app.route("/todo/delete/<int:pk>")
def delete(pk):
    info = todo.query.filter_by(id=pk).first()
    db.session.delete(info)
    db.session.commit()
    return redirect('/')



@login_required
@app.route("/todo/done/<int:pk>")
def donesr(pk):
    info = todo.query.filter_by(id=pk).first()
    info.todo_status = True
    db.session.add(info)
    db.session.commit()
    return redirect('/')


@login_required
@app.route("/todo/undone/<int:pk>")
def undone(pk):
    info = todo.query.filter_by(id=pk).first()
    info.todo_status = False
    db.session.add(info)
    db.session.commit()
    return redirect('/')

@login_required
@app.route("/todo/donesr/<int:pk>")
def done(pk):
    info = todo.query.filter_by(id=pk).first()
    info.todo_status = True
    db.session.add(info)
    db.session.commit()
    return redirect('/search')

@login_required
@app.route("/todo/undonesr/<int:pk>")
def undonesr(pk):
    info = todo.query.filter_by(id=pk).first()
    info.todo_status = False
    db.session.add(info)
    db.session.commit()
    return redirect('/search')

@login_required
@app.route('/search', methods=['GET','POST'])
def search():
    query = request.args.get('query')
    if query:
        results = todo.query.filter(todo.todo_task.ilike(f'%{query}%'),todo.user_id==current_user.id).all()
        
    else:
        results = [] 

    return render_template('sr.html', query=query, results=results,name=current_user.username)







