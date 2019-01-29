from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, IntegerField
from wtforms.validators import DataRequired, Length


class PaymentForm(FlaskForm):
    amount_money = DecimalField('amount_money', validators=[DataRequired()])
    number_invoice_provider = StringField(
        'number_invoice_provider',
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )
    number_invoice_reciever = StringField(
        'number_invoice_reciever',
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )


class PaymentPerformForm(FlaskForm):
    key = StringField(
        'key',
        validators=[
            DataRequired(),
            Length(5)
        ]
    )
