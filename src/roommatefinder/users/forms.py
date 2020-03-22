from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from roommatefinder.models import User

class LoginForm(FlaskForm):
    netid = StringField('netid',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    
    netid = StringField('netid',validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    gender = SelectField('gender:',
                        choices=[('F','F'), ('M','M'), ('O', 'O')], validators=[DataRequired()])
    year = SelectField('graduating year:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], validators=[DataRequired()])
    smoking = SelectField('Do you smoke?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    sleeping = SelectField('What time do you go to bed?',
                        choices=[('10','10PM'), ('12','12AM'), ('2', '2AM')], validators=[DataRequired()])
    waking = SelectField('What time do you generally wake up?',
                        choices=[('8','8AM'), ('10','10AM'), ('12', '12PM')], validators=[DataRequired()])
    room_utility = SelectField('What is your room utility?',
                        choices=[('study','study'), ('social','social')], validators=[DataRequired()])
    on_campus = SelectField('Do you want to live on campus?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_netid(self,field):
        if User.query.filter_by(netid=field.data).first():
            raise ValidationError('Your netid has been registered already!')


class UpdateUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    gender = SelectField('gender:',
                        choices=[('F','F'), ('M','M'), ('O', 'O')], validators=[DataRequired()])
    year = SelectField('graduating year:',
                        choices=[(2020,'2020'), (2021,'2021'), (2022, '2022'), (2023, '2023'), (2024, '2024')], validators=[DataRequired()])
    smoking = SelectField('Do you smoke?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    sleeping = SelectField('What time do you go to bed?',
                        choices=[(10,'10PM'), (12,'12AM'), (2, '2AM')], validators=[DataRequired()])
    waking = SelectField('What time do you generally wake up?',
                        choices=[(8,'8AM'), (10,'10AM'), (12, '12PM')], validators=[DataRequired()])
    room_utility = SelectField('What is your room utility?',
                        choices=[('study','study'), ('social','social')], validators=[DataRequired()])
    on_campus = SelectField('Do you want to live on campus?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
