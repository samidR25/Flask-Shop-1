from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
    username= StringField(label='username:', validators=[DataRequired(), Length(min=3, max =30)])
    email = StringField("email:", validators=[DataRequired(), Email()])
    password= PasswordField(label='password:',validators=[DataRequired(), Length(min=6)])
    submit= SubmitField(label='Register:')

##
class LoginForm(FlaskForm):
    username= StringField(label='username:', validators=[DataRequired()])
    password= PasswordField(label='password:', validators=[DataRequired()])
    submit= SubmitField(label='Login')

class SortItems(FlaskForm):
    sort_type = SelectField("Sort by", choices=[("price_high", "High price"),("price_low", "Low price"),("eco_low","Low Eco")],
     default="price_high",
     render_kw={"onchange": "this.form.submit()"})

class CheckoutForm(FlaskForm):
    name = StringField('name', validators=[DataRequired('Enter your Full Name'), Length(min=3, max=15)])
    address = StringField('address', validators=[DataRequired('Enter your Address')])
    card_no = PasswordField('card_no', validators=[DataRequired('Please enter your 16-digit card number'), Length(min=16, max=16)])
    submit = SubmitField('Checkout')








##
