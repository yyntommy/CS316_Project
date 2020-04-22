from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from roommatefinder.models import User

class FilterForm(FlaskForm):

    year_from = SelectField('Graduation Year From:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')])
    year_to = SelectField('To:',
                        choices=[('2020','2020'), ('2021','2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')])
    sleeping_from = TimeField('Sleep Time From:')
    sleeping_to = TimeField('To:')
    waking_from = TimeField('Wake Up Time From:')
    waking_to = TimeField('To:')
    room_type = SelectField('Room Type:',
    					choices=[('None', 'No Preference'), ('Study', 'Study'), ('Social','Social')])
    on_campus = SelectField('On Campus: ',
    					choices=[('None', 'No Preference'), ('Y', 'Y'), ('N', 'N')])
    gender = SelectField('Gender: ',
    					choices=[('None', 'No Preference'), ('M', 'M'), ('F', 'F')])
    smoking = SelectField('Smoking: ',
    					choices=[('None', 'No Preference'), ('Y', 'Y'), ('N', 'N')])
    submit = SubmitField('Filter')
