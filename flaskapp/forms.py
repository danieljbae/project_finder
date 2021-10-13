
""" Defines Forms: form fieldset and validation logic """

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

# Manages user sessions
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from flaskapp.models import Users, Languages, Careers

# There are 2 valid email formats: <identikey>@colorado.edu and <first>.<last>@colorado.edu
coloradoEmail_regex = "(?:\w+\.\w+|\w{4}\d{4})@colorado\.edu"


class RegistrationForm(FlaskForm):
    """ RegistrationForm Fieldset and Field validation logic """
    firstname = StringField(label='First Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=15)
                                        ]
                            )
    lastname = StringField(label='Last Name',
                           validators=[DataRequired(),
                                       Length(min=1, max=15)
                                       ]
                           )

    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email(),
                                    validators.Regexp(coloradoEmail_regex)
                                    ]
                        )
    password = PasswordField(label='Password',
                             validators=[DataRequired()]
                             )
    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')
                                                 ]
                                     )

    submit = SubmitField(label='Sign Up')

    def validate_email(self, email):
        """ Validate email, is unique to Users table """
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists, choose a different email')


class LoginForm(FlaskForm):
    """ LoginForm Fieldset and Field validation logic """
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email(),
                                    validators.Regexp(coloradoEmail_regex)
                                    ]
                        )
    password = PasswordField(label='Password',
                             validators=[DataRequired()]
                             )
    submit = SubmitField(label='Login')
    remember = BooleanField(label='Remember Me')


class UpdateAccountForm(FlaskForm):
    """  UpdateAccount Fieldset and Field validation logic """
    firstname = StringField(label='First Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=15)
                                        ]
                            )
    lastname = StringField(label='Last Name',
                           validators=[DataRequired(),
                                       Length(min=1, max=15)
                                       ]
                           )
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email(),
                                    validators.Regexp(coloradoEmail_regex)
                                    ]
                        )
    picture = FileField(label='Update profile picture',
                        validators=[FileAllowed(['jpg', 'png'])]
                        )
    submit = SubmitField('Update')

    def validate_email(self, email):
        """ Validate email: is unique to Users table and Different than old email """
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists, choose a different email')


class ProjectForm(FlaskForm):
    """  ProjectForm Fieldset and Field validation logic """
    title = StringField(label='Title', validators=[DataRequired()])
    content = TextAreaField(label='Content', validators=[DataRequired()])

    # Query tables to load multiple choice options
    languages_choices = [(row.id, row.name) for row in Languages.query.all()]
    languages = SelectMultipleField(u'Top programming languages in project', choices=languages_choices, coerce=int)
    careers_choices = [(row.id, row.name) for row in Careers.query.all()]
    careers_field = SelectMultipleField(u'Project members developer types', choices=careers_choices, coerce=int)
    submit = SubmitField('Post')
