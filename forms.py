from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class AuthForm(FlaskForm):
    api_key = StringField(
        'api_key',
        validators=[
            DataRequired("Key don't send"),
            Length(max=16, message='Character limit exceeded')
        ]
    )
