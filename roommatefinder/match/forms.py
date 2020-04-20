from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms_components import TimeField
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
    sleeping_from = TimeField('Sleeping time from')
    sleeping_to = TimeField('Sleeping time to')
    waking_from = TimeField('Waking time from')
    waking_to = TimeField('Waking time to')
    submit = SubmitField('Filter!')
