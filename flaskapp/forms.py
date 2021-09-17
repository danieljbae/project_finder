# source: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/03-Forms-and-Validation

'''Define fieldset and validation logic '''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
import email_validator
from flaskapp.models import Users, Languages, Careers

# 2-layer regex email validation: standard via Email() + regexp @colorado.edu
coloradoEmail_regex = "(?:\w+\.\w+|\w{4}\d{4})@colorado\.edu"

class RegistrationForm(FlaskForm):
    """ RegistrationForm Fieldset """
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=15)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=1, max=15)])

    email = StringField('Email', 
                        validators=[DataRequired(), Email(), validators.Regexp(coloradoEmail_regex)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    


    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        ''' Validate email is: unique '''
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists, choose a different email')


class LoginForm(FlaskForm):
    """ LoginForm Fieldset """
    email = StringField('Email',
                        validators=[DataRequired(), Email(), 
                                    validators.Regexp(coloradoEmail_regex)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')



class UpdateAccountForm(FlaskForm):
    """ Account Update Fieldset """
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=15)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=1, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), validators.Regexp(coloradoEmail_regex)])
    picture = FileField('Update profile picture',
                            validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_email(self, email):
        ''' Validate email is: is unique + different '''
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists, choose a different email')



class ProjectForm(FlaskForm):
    """ Project creation """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    choices_languages = [(row.id, row.name) for row in Languages.query.all()]
    languages = SelectMultipleField(u'Top programming languages in project', choices=choices_languages, coerce=int)

    choices_careers = [(row.id, row.name) for row in Careers.query.all()]
    careers_field = SelectMultipleField(u'Project members developer types', choices=choices_careers, coerce=int)

    submit = SubmitField('Post')