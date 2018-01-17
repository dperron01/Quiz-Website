from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from Quiz_app import db,app
import datetime
from sqlalchemy import CheckConstraint

class User(db.Model):
	__tablename__ = 'users'
	userID        = db.Column(db.Integer,     primary_key = True)
	firstname     = db.Column(db.String(100))
	lastname      = db.Column(db.String(100))
	email         = db.Column(db.String(120), unique=True)
	phone         = db.Column(db.String(15))
	pwdhash       = db.Column(db.String(200))
	authenticated = db.Column(db.Boolean,         default =False)
	registered_on_app   = db.Column(db.DateTime,   nullable=True)
	email_confirmed    = db.Column(db.Boolean,    nullable=True, default=False)
	email_confirmed_on = db.Column(db.DateTime,   nullable=True)
	Dp_filename        = db.Column(db.String,     nullable=True, default=None)
	Dp_url             = db.Column(db.String,     nullable=True, default=None)
	user_level = db.Column(db.Integer, default = 1)
	role = db.Column(db.String(50), default = 'user')
#	user_level = db.Column(db.Integer, default = 1)
	#Feedback = db.relationship('QuizDatabase', secondary = Feedback, backref = db.backref('comments', lazy = 'dynamic'))
	#TestRecord = db.relationship('QuizDatabase', secondary = TestRecord, backref = db.backref('testR', lazy = 'dynamic'))
	#PointsRecord = db.relationship('QuizTopic', secondary = PointsRecord, backref = db.backref('points', lazy = 'dynamic'))

	# Added column 'user_level' to see what level a user is on.
	# Need CheckConstraint on it?
	# It will be updated automatically, though
	################################################################

	def __init__(self, firstname, lastname, email, phone, password,role='user'):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.phone = phone
		self.set_password(password)
		self.authenticated = False
		self.registered_on_app = datetime.datetime.now()
		self.email_confirmed = False
		self.email_confirmed_on = None
		self.Dp_filename = None
		self.role = role
		#   self.user_level = 1
		#self.Dp_url = Dp_url

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def is_authenticated(self):
	#"""Return True if the user is authenticated."""
		return self.authenticated

	def is_anonymous(self):
	#"""Always False, as anonymous users aren't supported."""
		return False

	def is_active(self):
	#"""Always True, as all users are active."""
		return True

	def get_id(self):
	#"""Return the email address to satisfy Flask-Login's requirements."""
	#"""Requires use of Python 3"""
		return str(self.userID)


class QuizDatabase(db.Model):
    __tablename__ = 'quiz_database'
    #__searchable__ = ['topic_Name']
    topic_ID  = db.Column(db.Integer,    primary_key = True)
    topic_Name = db.Column(db.String(20), nullable = False, unique = True)
    topic_Desc = db.Column(db.String(150))
    topic_approved = db.Column(db.Boolean, default = False)
    admin_comment = db.Column(db.String(), nullable= True)
    topic_TotalLike = db.Column(db.Integer, default = 0, nullable = False)
    topic_TotalDislike = db.Column(db.Integer, default = 0, nullable = False)

    def __init__(self, topic_Name, topic_Desc,topic_approved=False):
    	self.topic_Name = topic_Name.lower()
    	self.topic_Desc = topic_Desc.lower()
    	self.topic_approved = topic_approved
    	self.topic_TotalLike = 0;
    	self.topic_TotalDislike = 0;

    def __unicode__(self):
        return self.topic_Name

    def __repr__(self):
        return '{}'.format(self.topic_Name)


class QuizTopic(db.Model):
    __tablename__ = 'quiz_topic'
    ques_ID     = db.Column(db.Integer,     primary_key = True )
    topic_ID    = db.Column(db.Integer,     db.ForeignKey('quiz_database.topic_ID'))
    topic_Name  = db.Column(db.String(20),  db.ForeignKey('quiz_database.topic_Name'))
    ques_Status = db.Column(db.String(10),  default = 'pending')
    ques        = db.Column(db.String(500), nullable = False, unique = True)
    optA        = db.Column(db.String(500), nullable = False, default = '---')
    optB        = db.Column(db.String(500), nullable = False, default = '---')
    optC        = db.Column(db.String(500), nullable = False, default = '---')
    optD        = db.Column(db.String(500), nullable = False, default = '---')
    answer      = db.Column(db.String(1),   nullable = False, default = '---')

    def __init__(self, topic_ID, ques, optA, optB, optC, optD, answer):
    	self.topic_ID = topic_ID
    	self.ques=ques
    	self.optA=optA
    	self.optB=optB
    	self.optC=optC
    	self.optD=optD
    	self.answer=answer


#    __table_args__ = (
#        CheckConstraint(ques_Status == 'Approved' OR ques_Status == 'Pending' OR ques_Status == 'Rejected', name='check_user_level'),
#        {})
# missing: check constraint, sequence for ques_ID

class Feedback(db.Model):
	__tablename__='feedback'
	feedback_ID = db.Column(db.Integer,      primary_key = True)
	topic_ID = db.Column(db.Integer,         db.ForeignKey('quiz_database.topic_ID'))
	UserID = db.Column(db.Integer,           db.ForeignKey('users.userID'))
	user_Comment = db.Column(db.String(200),  nullable = True)
	upVotes = db.Column(db.Integer,           nullable = False, default = 0)
	downVotes = db.Column(db.Integer,         nullable = False, default = 0)

	def __init__(self, topic_ID, UserID, user_Comment, upVotes, downVotes):
		self.topic_ID = topic_ID
		self.UserID =UserID
		self.user_Comment=user_Comment
		self.upVotes=upVotes
		self.downVotes=downVotes

     #__table_args__ = (
    #CheckConstraint(user_level > 0 AND user_level < 7, name='check_user_level'),
    #{})

class TestRecord(db.Model):
    __tablename__= 'test_record'
    test_ID   =  db.Column(db.Integer,     primary_key = True)
    userID    =  db.Column(db.Integer,     db.ForeignKey('users.userID'))
    topic_ID  =  db.Column(db.Integer,     db.ForeignKey('quiz_database.topic_ID'))
    test_Date =  db.Column(db.DateTime,    nullable = False)
    test_Result= db.Column(db.Integer,     nullable = False)

    def __init__(self, userID, topic_ID, test_Date, test_Result):
        self.userID  = userID
        self.topic_ID= topic_ID
        self.test_Date = test_Date
        self.test_Result = test_Result

class PointsRecord(db.Model):
    __tablename__ = 'points_record'
    userID = db.Column(db.Integer,    db.ForeignKey('users.userID'), primary_key = True)
    ques_ID= db.Column(db.Integer,    db.ForeignKey('quiz_topic.ques_ID') ,nullable=True, default=None)
    points = db.Column(db.Integer ,default=0)

    def __init__(self, userID, ques_ID=None, points=0):
        self.userID = userID
        self.ques_ID = ques_ID
        self.points = points

# Needs Composite Primary Key
