from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class SignUpForm(FlaskForm):
    """ Sign up for a user account """

    firstName = StringField(
        'First Name',
        [DataRequired()]
    )
    lastName = StringField(
        'Last Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            # Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    confirmPassword = PasswordField(
        'Repeat Password',
        [
            EqualTo('password', message='Passwords must match.')
        ]
    )
    birthday = DateField('Your Birthday')
    submit = SubmitField('Submit')
