from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditProfileForm():
    firstName = StringField('Username', validators=[Length(0, 64)]) 
    about_me = TextAreaField('About me ', validators=[Length(min=10, max=300)] )
    submit = SubmitField('Submit')

