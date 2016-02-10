import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string, redirect, url_for
import flask_wtf as WTF
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

from flask_login import LoginManager, login_user, current_user, UserMixin

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

## CONFIGURE APP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_PATH, 'login_example.db')
app.config['SECRET_KEY'] = 'keeping it real 4 life'

# ADD EXTENTIONS
login_manager = LoginManager(app)
db = SQLAlchemy(app)

# CONFIGURE EXTENSIONS
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return db.session.query(User).filter(User.username == username).first()


@app.before_first_request
def create_user():
    user = db.session.query(User).filter(User.username == 'mike').first()
    if not user:
        new_user = User('mike', 'mike', 'mike@mike.com')
        db.session.add(new_user)
        db.session.commit()


# TEMPLATES
login_template = '''
<form action="{{ url_for('login') }}" method="POST" name="login_user_form">
    {{ form.csrf_token }}

    {{ form.username() }}
    {{ form.password() }}
    {{ form.submit() }}

</form>
'''
index_template = '''
{% if current_user.is_authenticated %}
    <span style='color:#080; background:#efe;'>
        <i class='fa fa-check-circle'></i>
        You are logged in
    </span>
{% else %}
    <span style='color:#800; background:#fee;'>
        <i class='fa fa-times-circle'></i>
        login failed
    </span>
{% endif %}

{{ current_user.is_authenticated }}
'''

@app.route('/', methods =['GET'])
def index():
    return render_template_string(index_template)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        print (current_user.is_authenticated)
        login_user(user)
        print (current_user.is_authenticated)
        return redirect(url_for('index'))
    return render_template_string(login_template, form=form)


class LoginForm(WTF.Form):
    username = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__(self ,username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.username)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


if __name__ == '__main__':
    if os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]):
        app.run(debug=True)
    else:
        db.create_all()
        app.run()
