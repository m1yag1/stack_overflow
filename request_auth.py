## Example app for Stack Overflow Question
## https://stackoverflow.com/questions/33106298/is-it-possible-to-use-flask-logins-authentication-as-simple-http-auth-for-a-res/33111714#33111714

from functools import wraps

from flask import (Flask,
                   jsonify,
                   redirect,
                   render_template_string,
                   Response,
                   request,
                   session,
                   url_for
                   )

from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import Required
import flask_wtf as WTF

app = Flask(__name__)


app.debug = True
app.config['SECRET_KEY'] = 'abracadabara'

login_template = '''
<form action="{{ url_for('login') }}" method="POST" name="login_user_form">
    {{ form.csrf_token }}

    {{ form.email() }}
    {{ form.password() }}
    {{ form.submit() }}

</form>
'''




def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin@admin.com' and password == 'secret'


def bad_auth():
    """Sends an error response"""
    return jsonify(dict(message='incorrect username or password'))


def load_user_from_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if 'is_authenticated' in session:
            # allow user through this could be
            return f(*args, **kwargs)
        if auth and check_auth(auth.username, auth.password):
            username = auth.username
            password = auth.password
            return f(*args, **kwargs)
        else:
            return bad_auth()

    return decorated


@app.route('/')
def index():
    return jsonify(dict(message='hello world'))


@app.route('/success')
@load_user_from_request
def success():
    return jsonify(dict(message='Great Success!'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.email.data
            password = form.password.data
            if check_auth(username, password):
                session['is_authenticated'] = True
                return redirect(url_for('success'))
            else:
                return bad_auth()
    return render_template_string(login_template, form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


class LoginForm(WTF.Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run()
