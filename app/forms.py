from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email(), Length(max=320)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Entrar")
