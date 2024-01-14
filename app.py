from flask import Flask , render_template , request , url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError
import os
from flask_bcrypt import Bcrypt
import sqlite3
import pickle

# model=pickle.load(open('model.pkl','rb'))

file_path = os.path.abspath(os.getcwd())+"\database.db"



app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname= db.Column(db.String(20), nullable=False)
    secondname = db.Column(db.String(20), nullable=False)
    email= db.Column(db.String(20), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    username= db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname= db.Column(db.String(20), nullable=False)
    secondname = db.Column(db.String(20), nullable=False)
    email= db.Column(db.String(20), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    username= db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname= db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    age= db.Column(db.Float(20), nullable=False)
    weight = db.Column(db.Float(20), nullable=False)
    height= db.Column(db.Float(20), nullable=False)

class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    secondname = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
    phonenumber = StringField('Phone', validators=[InputRequired(), Length(min=4, max=20)])
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)])
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

class PatientForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    lastname = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    age = StringField(validators=[InputRequired(), Length(min=1, max=20)])
    weight = StringField( validators=[InputRequired(), Length(min=1, max=20)])
    height = StringField( validators=[InputRequired(), Length(min=1, max=20)])

    
    submit = SubmitField("SUBMIT")

        
with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                flash("You have been logged in successfully")
                login_user(user)
                if current_user.username == 'gichuki_cynthia':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
            
            else:
                flash("User does not Exist")

    return render_template("login.html", form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(firstname=form.firstname.data, lastname=form.secondname.data, email=form.email.data, phonenumber=form.phonenumber.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PatientForm()

    if form.validate_on_submit():
        new_patient = Patient(firstname=form.firstname.data, lastname=form.lastname.data, age=form.age.data, weight=form.weight.data, height=form.height.data)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('login'))
    
    prediction = model.predict_proba
    
    return render_template("index.html", form=form)





@app.route('/admin', methods=['GET', 'POST'])
#@login_required
def admin():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(firstname=form.firstname.data, lastname=form.secondname.data, email=form.email.data, phonenumber=form.phonenumber.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User added Successfully")

    connection = sqlite3.connect("database.db")
    connection.row_factory=sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * from patient")
    patient = cursor.fetchall()
    connection.close()

    connection = sqlite3.connect("database.db")
    connection.row_factory=sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * from user")
    user = cursor.fetchall()
    connection.close()


    return render_template("admin.html", patient=patient, user=user, form=form)

    
   
    #if current_user.username == 'gichuki_cynthia':
    #    return redirect(url_for('admin'))
    



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    #flash("You have been logged out successfully")
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)

    


    




