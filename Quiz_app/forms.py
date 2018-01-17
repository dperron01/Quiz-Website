from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, TextField, BooleanField, PasswordField, SelectField, FieldList, RadioField, FormField,HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, AnyOf, Regexp, Required
#from wtforms_components import If
from flask_wtf.file import FileField, FileRequired, FileAllowed

class SignupForm(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired('First name required')])
	last_name = StringField('Last name', validators=[DataRequired('Last name required')])
	email = TextField('Email',validators=[DataRequired("Please enter email."), Email("Please enter valid email address.")])
	phone_no = StringField('Phone Number',validators=[Regexp('^\s*(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\s*$',message="Use XXX-XXX-XXXX Format")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	re_password = PasswordField('Confirm Password', validators=[DataRequired("Please enter a password."), EqualTo('password',message='Password did not match!')])
	remember_me = BooleanField('remember_me', default=False)
	submit = SubmitField('Sign Up')

#phone numbers currently accepting canadian format with regexp and can be changed for international format
#Can also apply Length(min=10, max=15) format to phone numbers

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter valid email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please Enter Your Account Password.")])
  remember_me = BooleanField('Keep me logged in:', default=False)
  submit = SubmitField("Sign In")

class PasswordResetForm(FlaskForm):
	email = StringField('Email:', validators=[DataRequired("Please enter your email address."), Email("Please enter valid email address.")])
	submit = SubmitField("Submit")

class Password_EmailForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	re_password = PasswordField('Confirm Password', validators=[DataRequired("Please enter a password."), EqualTo('password',message='Password did not match!')])
	submit = SubmitField("Submit")

## Added by Harjot on July 23rd
class updateProfileForm(FlaskForm):
  first_name = StringField('First name', validators=[DataRequired('First name required')])
  last_name = StringField('Last name', validators=[DataRequired('Last name required')])
  email = TextField('Email',validators=[DataRequired("Please enter your email address."), Email("Please enter valid email address.")])
  phone_no= StringField('Phone Number',validators=[Regexp('^\s*(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\s*$',message="Please Enter XXX-XXX-XXXX Format")])
  submit = SubmitField('Update')

class DeleteForm(FlaskForm):
   email = StringField('Email:', validators=[DataRequired("Please enter your email address."), Email("Please enter valid email address.")])
   password = PasswordField('Password:', validators=[DataRequired("Please enter a password.")])
   delete = SubmitField('Delete')

class QuestionForm(FlaskForm):
	question =  TextAreaField('Question', validators=[DataRequired('*required')])
	opta = StringField('Option A', validators=[DataRequired('*required')])
	optb = StringField('Option B',validators=[DataRequired('*required')])
	optc = StringField('Option C',validators=[DataRequired('*required')])
	optd = StringField('Option D',validators=[DataRequired('*required')])
	answer = SelectField('Correct Option', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
	submit = SubmitField('Submit Question')

class PhotoForm(FlaskForm):
	photo = FileField('image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class SearchForm(FlaskForm):
	search = StringField('search',validators=[DataRequired()])
	submit = SubmitField()

class CreateTopic(FlaskForm):
	topic_name = StringField('Topic Name', validators=[DataRequired('Topic Name required')])
	topic_description = StringField('Topic Description',  validators=[DataRequired('Description required')])
	submit = SubmitField('Submit Topic')

class QuestForm(FlaskForm):
	bart = RadioField(default='A',validators=[Required()])
	ques_ID = -1

class QuizForm(FlaskForm):
	questions = FieldList(FormField(QuestForm))

class RateQuizForm(FlaskForm):
	rating = RadioField('Rate this quiz', choices=[('1','I like this quiz'),('2',"I don't like this quiz")])
	comment =  TextAreaField('Comment')

class Admin_NewRequest(FlaskForm):
	topic_id = IntegerField('Topic ID:',validators= [DataRequired('Please Enter Topic ID')])
	#ques_id =  IntegerField('Question ID :',validators= [DataRequired('Please Enter Topic ID')])
	comment =  TextAreaField('Comment: ')
	#submit = SubmitField('submit')
	submit1 = SubmitField('Approved')
	submit2 = SubmitField('Delete')
