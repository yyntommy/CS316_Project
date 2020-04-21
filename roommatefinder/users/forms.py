from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms_components import TimeField
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from roommatefinder.models import User

class LoginForm(FlaskForm):
    netid = StringField('netid',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):

    netid = StringField('NetId:',validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    gender = SelectField('Gender:',
                        choices=[('F','F'), ('M','M'), ('O', 'O')], validators=[DataRequired()])
    year = SelectField('Graduating Year:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], validators=[DataRequired()])
    smoking = SelectField('Do you smoke?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    sleeping = TimeField('What time do you usually go to bed?', validators=[DataRequired()])
    waking = TimeField('What time do you usually wake up?', validators=[DataRequired()])
    room_utility = SelectField('Do you see the room as more of a social or study place?',
                        choices=[('Study','Study'), ('Social','Social')], validators=[DataRequired()])
    on_campus = SelectField('Do you want to live on campus?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    password = PasswordField('Password:',validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password:',validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_netid(self,field):
        if User.query.filter_by(netid=field.data).first():
            raise ValidationError('Your netid has been registered already!')


class UpdateUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender:',
                        choices=[('F','F'), ('M','M'), ('O', 'O')], validators=[DataRequired()])
    year = SelectField('Graduating Year:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], validators=[DataRequired()])
    smoking = SelectField('Do you smoke?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    sleeping = TimeField('What time do you usually go to bed?')
    waking = TimeField('What time do you usually wake up?')
    room_utility = SelectField('Do you see the room as more of a social or study place?',
                        choices=[('Study','Study'), ('Social','Social')], validators=[DataRequired()])
    on_campus = SelectField('Do you want to live on campus?',
                        choices=[('Y','Y'), ('N','N')], validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
