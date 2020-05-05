from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    username = StringField('Nazwa uzytkownika', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Haslo', validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Zaloguj')

class Run(FlaskForm):
    submit1 = SubmitField('Wlacz serwer')

class Close(FlaskForm):
    submit2 = SubmitField('Wylacz serwer')

class Console(FlaskForm):
    submit3 = SubmitField('Konsola')
