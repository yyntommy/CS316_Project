from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from roommatefinder.models import User

class FilterForm(FlaskForm):

    year_from = SelectField('graduation year from:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], validators=[DataRequired()])
    year_to = SelectField('graduation year to:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], validators=[DataRequired()])
    sleeping_from = SelectField('Sleeping time from',
                        choices=[('22:00','22:00'), ('00:00','00:00'), ('2:00', '2:00')], validators=[DataRequired()])
    sleeping_to = SelectField('Sleeping time to',
                        choices=[('22:00','22:00'), ('00:00','00:00'), ('2:00', '2:00')], validators=[DataRequired()])
    waking_from = SelectField('Waking time from',
                        choices=[('8:00','8:00'), ('10:00','10:00'), ('12:00', '12:00')], validators=[DataRequired()])
    waking_to = SelectField('Waking time to',
                        choices=[('8:00','8:00'), ('10:00','10:00'), ('12:00', '12:00')], validators=[DataRequired()])
    submit = SubmitField('Filter!')
