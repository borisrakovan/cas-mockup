from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, URL, Optional


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    service = StringField('Služba', validators=[URL(require_tld=False), Optional()])

    submit = SubmitField('Prihlásiť sa')