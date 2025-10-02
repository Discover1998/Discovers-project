from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Email, Regexp, EqualTo, DataRequired, Length
import data.person_number_checker

class RegistrationForm(FlaskForm):
    person_number = StringField("Person Number", validators=[DataRequired(), Length(min=10, max=13)])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=25)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    #username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    address = StringField("Address", validators=[DataRequired(), Length(min=2, max=25)])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=2, max=10)])

    submit = SubmitField("Sign Up")
"""
    def validate_person_number(self, field):
        value = field.data.strip()
        if not personnummer_checker(value):
            raise ValidationError("Invalid personnummer.")
"""

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


"""
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$",
                message="Password must be 8–32 characters, include at least one uppercase, one lowercase, one number, and one special character."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
"""
