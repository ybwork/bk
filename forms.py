from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, IntegerField
from wtforms.validators import DataRequired, Length


class PaymentForm(FlaskForm):
    amount_money = DecimalField('amount_money', validators=[DataRequired()])
    invoice_provider = StringField(
        'invoice_provider',
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )
    invoice_reciever = StringField(
        'invoice_reciever',
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )


