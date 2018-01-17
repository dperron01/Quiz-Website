from Quiz_app import app
from Quiz_app import db
from Quiz_app.models import User, QuizDatabase, QuizTopic, PointsRecord, Feedback, TestRecord
import sys, os, datetime

if os.path.abspath(os.curdir) not in sys.path:
	sys.path.append(os.path.abspath(os.curdir))

with app.app_context():
	db.drop_all()
	db.create_all()

	#Initializing db with admin and users
	admin = User(firstname='admin', lastname='user', email='admin@pquiz.com', phone='123-123-1234',
		password='123456', role='admin')
	user1 = User(firstname='john', lastname='doe', email='ex1@pquiz.com', phone='123-123-1234',
		password='123456', role='user')
	user2 = User(firstname='peter', lastname='last', email='ex2@pquiz.com', phone='123-123-1234',
		password='123456', role='user')

	admin.authenticated = True
	admin.email_confirmed = True
	user1.authenticated = True
	user1.email_confirmed = True
	user1.Dp_filename = "[1]profile.jpg"
	user2.authenticated = True
	user2.email_confirmed = True

	db.session.add(admin)
	db.session.add(user1)
	db.session.add(user2)
	db.session.commit()

	#Intializing points to the  new user
	points2 = PointsRecord(userID=2, points=50)
	points3 = PointsRecord(userID=3, points=50)
	db.session.add(points2)
	db.session.add(points3)
	db.session.commit()

	#Initializing db with topics
	topic1 = QuizDatabase(topic_Name='flask',topic_Desc='python framework')
	topic2 = QuizDatabase(topic_Name='pizza',topic_Desc='food')
	topic3 = QuizDatabase(topic_Name='larval',topic_Desc='php framework')
	topic4 = QuizDatabase(topic_Name='Relativity',topic_Desc='Einstein topic in physics')
	topic5 = QuizDatabase(topic_Name='service tax',topic_Desc='finance')
	topic6 = QuizDatabase(topic_Name='SFU Professors',topic_Desc='Computing Science Department')

	db.session.add(topic1)
	db.session.add(topic2)
	db.session.add(topic3)
	db.session.add(topic4)
	db.session.add(topic5)
	db.session.add(topic6)

	db.session.commit()

	#Initializing db with questions on available topics
	ques1 = QuizTopic(topic_ID=1,ques='If you have debug disabled on your network, the server can be made publicly available by changing the call of the run() method to?',optA='app.run()',optB='app.run(host=0.0.0.0)',optC='app.host(0.0.0.1)',optD='app.host()',answer='A')
	ques2 = QuizTopic(topic_ID=2,ques='Pizza is invented by which famous personality?',optA='Greg Baker',optB='Mahya',optC='Team Peer Quiz',optD='Cmpt 470',answer='C')
	ques3 = QuizTopic(topic_ID=1,ques='which framework from the following is a micro-framework',optA='pyramid',optB='Django',optC='flask',optD='python',answer='C')
	ques4 = QuizTopic(topic_ID=1,ques='Flask was the most popular web framework in 2015.',optA='True',optB='False',optC='It depends on personal perspective',optD='who cares!',answer='A')

	db.session.add(ques1)
	db.session.add(ques2)
	db.session.add(ques3)
	db.session.add(ques4)

	db.session.commit()

	#Initializing db with feedback on available topics
	feed1 = Feedback(topic_ID=1, UserID=2, user_Comment='What a nice quiz!', upVotes=0, downVotes=0)
	feed2 = Feedback(topic_ID=2, UserID=3, user_Comment='Terrible quiz!', upVotes=0, downVotes=0)
	feed3 = Feedback(topic_ID=1, UserID=2, user_Comment='This quiz was too easy.', upVotes=0, downVotes=0)
	feed4 = Feedback(topic_ID=2, UserID=3, user_Comment='I liked this quiz!', upVotes=0, downVotes=0)
	feed5 = Feedback(topic_ID=3, UserID=2, user_Comment='I feel I learned something!', upVotes=0, downVotes=0)

	db.session.add(feed1)
	db.session.add(feed2)
	db.session.add(feed3)
	db.session.add(feed4)
	db.session.add(feed5)

	db.session.commit()

	#Initializing db with test history on available topics
	test1 = TestRecord(userID=1, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)
	test2 = TestRecord(userID=1, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=6)
	test3 = TestRecord(userID=1, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=3)
	test4 = TestRecord(userID=1, topic_ID=3, test_Date=datetime.datetime.now().date(), test_Result=5)
	test5 = TestRecord(userID=1, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)
	test6 = TestRecord(userID=2, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)
	test7 = TestRecord(userID=2, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=6)
	test8 = TestRecord(userID=2, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=3)
	test9 = TestRecord(userID=2, topic_ID=3, test_Date=datetime.datetime.now().date(), test_Result=5)
	test10 = TestRecord(userID=2, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)
	test11 = TestRecord(userID=3, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)
	test12 = TestRecord(userID=3, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=6)
	test13 = TestRecord(userID=3, topic_ID=2, test_Date=datetime.datetime.now().date(), test_Result=3)
	test14 = TestRecord(userID=3, topic_ID=3, test_Date=datetime.datetime.now().date(), test_Result=5)
	test15 = TestRecord(userID=3, topic_ID=1, test_Date=datetime.datetime.now().date(), test_Result=10)


	db.session.add(test1)
	db.session.add(test2)
	db.session.add(test3)
	db.session.add(test4)
	db.session.add(test5)
	db.session.add(test6)
	db.session.add(test7)
	db.session.add(test8)
	db.session.add(test9)
	db.session.add(test10)
	db.session.add(test11)
	db.session.add(test12)
	db.session.add(test13)
	db.session.add(test14)
	db.session.add(test15)

	db.session.commit()
