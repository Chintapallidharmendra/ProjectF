from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('UserName',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class updatePassword(FlaskForm):
    username = StringField('UserName',
                        validators=[DataRequired()])
    oldpassword = PasswordField('Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[ DataRequired(),EqualTo('newpassword')])
    submit = SubmitField('Update')
