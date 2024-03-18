from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField, RadioField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, Regexp
from database.database import search_user, search_user_name
from werkzeug.security import check_password_hash
from decimal import Decimal

category_choices = [('Cars', 'Cars'), ('Furniture', 'Furniture'), ('Electronics', 'Electronics'), ('Clothing', 'Clothing'), ('HomeGarden', 'Home & Garden'), ('BooksMedia', 'Books & Media'), ('Other', 'Other')]
conditions = ['New', 'Used', 'Spares or repair']

def strip_whitespace(form, field):
    if field.data:
      field.data = field.data.strip() 

def validate_password(form, field):
    user = search_user(form.email.data)
    if len(user) != 1 or not check_password_hash(user[0][3], field.data):
      raise ValidationError("Incorrect email or password")

def validate_email(form, field):
  if search_user(field.data):
      raise ValidationError("Email already exists")
   
def validate_username(form, field):
   if ' ' in field.data:
      raise ValidationError("Username cannot contain spaces")
   if search_user_name(field.data):
      raise ValidationError("Username already exists")

def validate_price(form, field):
  if field.data is None:
      raise ValidationError("Price is required")
  if not isinstance(field.data, Decimal):
      raise ValidationError("Price must be a number")
  if field.data < 0:
      raise ValidationError("Price must be a positive number")
  if field.data > 999999999:
      raise ValidationError("Price must be less than 999999999")
  if "." in str(field.data) and len(str(field.data).split('.')[1]) > 2:
      raise ValidationError("Price must have a maximum of 2 decimal places")

def validate_category(form, field):
  if field.data not in [choice[0] for choice in category_choices]:
     raise ValidationError("Invalid category")

def validate_condition(form, field):
  if field.data not in conditions:
     raise ValidationError("Invalid condition")


class RegistrationForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20), strip_whitespace, validate_username, ])
  email = StringField("Email", id="email-signup", validators=[DataRequired(), Email(), strip_whitespace, validate_email ])
  password = PasswordField("Password", id="password-signup", validators=[DataRequired(), Length(min=8), Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message="Password not matching criteria")])
  submit = SubmitField("Sign Up", id="submit-signup")

class SignInForm(FlaskForm):
  email = StringField("Email", id="email-signin", validators=[DataRequired(), Email(),  strip_whitespace])
  password = PasswordField("Password", id="password-signin", validators=[DataRequired(), validate_password])
  submit = SubmitField("Sign In", id="submit-signin")

class ListingForm(FlaskForm):
   title = StringField("Title", validators=[DataRequired(), Length(min=3, max=80), strip_whitespace])
   description = TextAreaField("Description", validators=[Length(min=0, max=250)])
   condition = RadioField("Condition", choices=[(condition, condition) for condition in conditions], validators=[DataRequired(), validate_condition])
   price = DecimalField("Price", validators=[NumberRange(min=1, max=999999999), DataRequired(), validate_price])
   category = SelectField("Options", choices=[("Select a Category", "Select a Category")] + category_choices, validators=[DataRequired(), validate_category])
   photo = FileField("Photo", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Only JPEG and PNG files are allowed')])
   submit = SubmitField("Post listing", id="submit-listing") 
