# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField,SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, URL, Optional, EqualTo

from app.models import Role


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    # password = PasswordField('Heslo', validators=[DataRequired()])
    service = StringField(u'Služba', validators=[URL(require_tld=False), Optional()])

    submit = SubmitField(u'Prihlásiť sa')


class CreateForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    # password = PasswordField('Heslo', validators=[DataRequired()])
    # repeat_password = PasswordField('Heslo znova', validators=[DataRequired(), EqualTo('password')])
    # first_name = StringField('Meno', validators=[DataRequired()])
    # surname = StringField('Priezvisko', validators=[DataRequired()])
    identity_id = StringField('Identity ID', validators=[DataRequired()])
    organization = StringField(u'Organizácia', validators=[DataRequired()])
    roles = SelectMultipleField('Role', coerce=int  )

    submit = SubmitField(u'Vytvoriť')

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.roles.choices = [(r.id, r.code) for r in Role.query.all()]
