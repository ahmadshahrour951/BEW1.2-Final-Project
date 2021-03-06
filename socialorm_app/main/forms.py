from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from socialorm_app.models import Institution, Residence
from wtforms.fields.html5 import DateField

class ProfileForm(FlaskForm):
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    institution = QuerySelectField(label='Institution', query_factory=lambda: Institution.query, allow_blank=False, get_label='name')
    residence = QuerySelectField(label='Residence', query_factory=lambda: Residence.query, allow_blank=False, get_label='name')
    dorm_room = StringField(label='Dorm Room', validators=[DataRequired(), Length(min=3, max=5)])
    status = StringField(label='Status', validators=[Length(min=0, max=30)])
    submit = SubmitField(label='Update')

    def validate_residence(self, residence):
        # Residence and Institution is a double bind, in order to mitigate, a custom validator is created for resdience
        # its pushing the responsiblity of the user to make the changes, however in the future this should be controlled by the developer to imporove expereience
        if residence.data.institution != self.institution.data:
          raise ValidationError(f'{residence.data.name} is not part of {self.institution.data.name}')
