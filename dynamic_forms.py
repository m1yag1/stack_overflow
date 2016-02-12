from flask import Flask, render_template, render_template_string
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DecimalField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'notdamomma'

login_template = '''
<form action="" method="post" name="login">
      {{ form.hidden_tag() }}
      <p>
          Please enter the expression:<br>
          {{ form.expression() }}<br>
      </p>
          Enter the value and respective error:<br>

          {{ form.ve_list[0][0] }}
          {{ form.ve_list[0][1] }}

      <p><input type="submit" value="Calculate"></p>
  </form>
'''


class Receiver(Form):
    expression = StringField('expression', validators=[DataRequired()])
    # ve_list = [[StringField('expreson'), DecimalField('expression', places=10)], [StringField('expreson'), DecimalField('expression', places=10)]]
    # remember_me = BooleanField('remember_me', default=False)

    ve_list = [[DecimalField('value', validators=[DataRequired()]), DecimalField('value', validators=[DataRequired()])]]


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Receiver(use_csrf=False)
    return render_template_string(login_template, form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=True)
