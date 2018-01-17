from . import app
from flask import render_template, request, session, redirect, url_for, flash, g,json,jsonify,abort
from Quiz_app.models import User, QuizDatabase, QuizTopic, Feedback, TestRecord, PointsRecord
from Quiz_app import db
from Quiz_app.forms import SignupForm, LoginForm, PasswordResetForm,Password_EmailForm, DeleteForm, QuestionForm, PhotoForm, updateProfileForm, SearchForm, CreateTopic,QuestForm, QuizForm, RateQuizForm, Admin_NewRequest
from sqlalchemy import exc, func, cast, DATE
from flask_login import login_required, login_user, logout_user, current_user
from Quiz_app.email import send_confirmation_email, password_reset_email
from itsdangerous import URLSafeTimedSerializer
from wtforms import RadioField
from wtforms.validators import Required
import datetime
from werkzeug import secure_filename
import os


@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  return render_template('index.html', form1 = LoginForm(), form2 = SignupForm(), form3 = updateProfileForm())

@app.route('/signup', methods = ['GET', 'POST'])
def new():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = SignupForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      try:
        new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.phone_no.data, form.password.data)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        send_confirmation_email(new_user)
        flash('Congratulations! Email has been sent to your provided email account for confirmation!', 'success')
        return redirect(url_for('login'))
      except exc.IntegrityError:
        db.session.rollback()
        flash("Email id already exists!!")
  return render_template('signup.html', form2= form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='too-salt-for-confirmation', max_age=3600)
    except:
        flash('OHH NO! The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.datetime.now()
        db.session.add(user)

        points = PointsRecord(userID=user.userID, points=50)
        db.session.add(points)

        db.session.commit()
        flash('Thank you for confirming your email address!')

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user is not None and user.email_confirmed and user.check_password(form.password.data):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data, force= True)
        flash('WELCOME, {}'.format(current_user.firstname))
        return redirect(url_for('home'))
      else:
        if user is None:
          flash('Please provide correct login credentials. Entered Email not found!', 'error')
        elif user.check_password(form.password.data) == False:
          flash('Please provide correct login credentials. Wrong Password Entered!', 'error')
        else:
          flash('Please confirm your email adrress first from your email account')


  return render_template('login.html', form=form, _external=True)

@app.route('/reset', methods = ['POST','GET'])
def password_reset():
  form = PasswordResetForm()
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(email=form.email.data).first()
      if user.email_confirmed:
        flash('Email has been sent for password reset. Please check your Email account!','success')
        password_reset_email(user)
        return redirect(url_for('login'))
      else:
        flash('Please confirm your initial email verification before attempting password reset!','error')
        return redirect(url_for('index'))
    except:
      flash('Entered Email Address is invalid!')
  return render_template('password_reset.html', form=form)

@app.route('/reset/<token>',methods = ['POST','GET'])
def reset_password_email(token):
    try:
        pwd_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = pwd_reset_serializer.loads(token, salt='too-too-too-salty-for-confirmation', max_age=3000)
    except:
        flash('OHH NO! The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))
    form = Password_EmailForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        try:
          print(email)
          user = User.query.filter_by(email=email).first()
          print(user.pwdhash)
          if user:
            user.set_password(form.password.data)
            print(form.password.data)
            print(user.pwdhash)
            db.session.add(user)
            db.session.commit()
            user.check_password(form.password.data)
            flash('Peer Quiz Account password has been updated.', 'info')
            return redirect(url_for('login'))
          else:
            flash('Email id not found!')
            return redirect(url_for('login'))
        except exc.IntegrityError:
          db.session.rollback()
          flash('Error')
      else:
        redirect(url_for('reset_password_email',token=token))
    return render_template('password_reset_form.html',form=form,token=token)

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Sayonara!!! Please Link Up Soon', 'info')
    return redirect(url_for('login'))

@app.route('/delete')
@login_required
def delacc():
   form = DeleteForm(request.form)
   return render_template('delete.html',form=form)

@app.route('/deleted', methods=['POST','GET'])
@login_required
def deldone():
   if request.method == 'POST':
      form = DeleteForm()
      em = form.email.data
      pas=form.password.data
      user = User.query.filter_by(email = em).first()
      if user and user.check_password(pas)==True:
         User.query.filter_by(email=em).delete()
         db.session.commit()
         return redirect(url_for('index'))
   return render_template('delete.html',form = DeleteForm(), message="account with provided email does not exists")

@app.route('/updateProfile', methods=['GET', 'POST'])
@login_required
def updateProfile():
    if request.method == 'GET':
       form = updateProfileForm(request.form)
       return render_template('updateProfile.html', form3=form)
    else:
        if request.method == 'POST':
          form = updateProfileForm(request.form)
          update_profile = User.query.filter_by(email = current_user.email).first()
          if form.validate_on_submit():
            try:
              update_profile.authenticated = True
              update_profile.firstname = form.first_name.data
              update_profile.lastname = form.last_name.data
              update_profile.email = form.email.data
              update_profile.phone = form.phone_no.data
              db.session.commit()
              send_confirmation_email(update_profile)
              flash('Profile Updated!', 'success')
              return redirect(url_for('account'))
            except exc.IntegrityError:
              db.session.rollback()
              flash("Could not update. Please try again later.")
        return render_template('account.html', form=PhotoForm(), message=current_user.firstname, user = update_profile)


@app.route('/home')
@login_required
def home():
    if current_user.role == 'admin':
        pending_topic = QuizDatabase.query.filter_by(topic_approved = False).count()
        pending_ques = QuizTopic.query.filter_by(ques_Status = 'pending').count()
        return render_template('user.html',form=SearchForm(), pending_ques=pending_ques, pending_topic=pending_topic)
    else:
        return render_template('user.html',form=SearchForm())        

@app.route('/admin')
@login_required
def admin():
  if current_user.role == 'admin':
    users = User.query.order_by(User.userID ).all()
    topics = QuizDatabase.order_by(QuizDatabase.topic_ID).all()
    quiz_questions = QuizTopic.order_by(QuizTopic.ques_ID).all()
    return render_template('admin.html')
  else:
    abort(403)

@app.route('/admin/all_users')
@app.route('/admin/all_users/<int:page>')
@login_required
def admin_all_users(page=1):
  if current_user.role == 'admin':
    users = User.query.order_by(User.userID ).paginate(page,10,False)
    return render_template('admin.all_users.html',users=users)
  else:
    abort(403)

@app.route('/admin/topic_approval',methods=['POST','GET'])
@app.route('/admin/topic_approval/<int:page>',methods=['POST','GET'])
@login_required
def admin_new_topic(page=1):
  if current_user.role == 'admin':
    topics = QuizDatabase.query.filter_by(topic_approved = False).paginate(page,1,False)
    pending_topic = QuizDatabase.query.filter_by(topic_approved = False).count()
    form = Admin_NewRequest()
    if request.method == 'POST':
      print(form.data)
      if form.validate_on_submit() and form.submit1.data:
        ID = form.topic_id.data
        topic = QuizDatabase.query.get(ID)
        print(topic)
        #points = PointsRecord.query.get(ID)
        if topic is None:
          flash('Hello Admin, Entered Topic ID does not exist')
        else:
          topic.topic_approved = True
          db.session.add(topic)
          #points.points = points.points + 5
          #db.session.add(points)
          db.session.commit()
        return redirect(url_for('admin_new_topic'))
      if form.validate_on_submit() and form.submit2.data:
        ID = form.topic_id.data
        try:
          QuizDatabase.query.filter_by(topic_ID=ID).delete()
          db.session.commit()
        except exc.IntegrityError:
          flash("Deleting this Topic Right Now not possible as already quiz questions exist on it!")
        return redirect(url_for('admin_new_topic'))
    return render_template('admin_new_topic.html',topics=topics,form=form, pending_topic=pending_topic)
  else:
    abort(403)

@app.route('/admin/ques_approval',methods=['POST','GET'])
@app.route('/admin/ques_approval/<int:page>',methods=['POST','GET'])
@login_required
def admin_new_ques(page=1):
  if current_user.role == 'admin':
    quiz_questions = QuizTopic.query.filter_by(ques_Status = 'pending').paginate(page,1,False)
    pending_ques = QuizTopic.query.filter_by(ques_Status = 'pending').count()
    if request.method == 'POST':
        ID = request.form['ques_id']
        ques = QuizTopic.query.get(ID)
        if ques is None:
          flash('Hello Admin, Entered Question ID does not exist')
        else:
          ques.ques_Status = request.form['ques_status']
          db.session.add(ques)
          db.session.commit()
        return redirect(url_for('admin_new_ques'))
    return render_template('admin_new_quiz.html',questions=quiz_questions,form=Admin_NewRequest(), pending_ques=pending_ques)
  else:
    abort(403)

@app.route('/quiz/create')
@app.route('/quiz/create/<int:page>',methods=['POST','GET'])
@login_required
def quiz_view_topics(page=1):
  topics = QuizDatabase.query.filter_by(topic_approved=True).order_by(QuizDatabase.topic_Name).paginate(page,5,False)
  return render_template("quiz_topics_view.html",message = current_user.firstname, topics=topics)

@app.route('/quiz/view/<topic>')
@login_required
def quiz_view_single_topic(topic):
  topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first()
  dicts = {}
  if  topic_ID == None:
    comments = " "
    return render_template("error_page.html", error ="Topic does not exist or has not been approved")
  else:
    topic_ID = topic_ID.topic_ID
    comments=Feedback.query.filter_by(topic_ID=topic_ID).limit(5).all()
    for comment in comments:
    	dicts[comment.UserID] = User.query.filter_by(userID=comment.UserID).first()
  return render_template("view_single_topic.html", topic=topic, comments=comments, dicts=dicts)

@app.route('/quiz/view/<topic>/comments')
@login_required
def quiz_view_comments(topic):
  topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first()
  dicts = {}
  if  topic_ID == None:
    comments = " "
    return render_template("error_page.html", error ="Topic does not exist or has not been approved")
  else:
    topic_ID = topic_ID.topic_ID
    comments=Feedback.query.filter_by(topic_ID=topic_ID).all()
    for comment in comments:
      dicts[comment.UserID] = User.query.filter_by(userID=comment.UserID).first()
  return render_template("view_comments.html", topic=topic, comments=comments, dicts=dicts)


@app.route('/quiz/create/topic', methods=['GET', 'POST'])
@login_required
def quiz_create_topic():
    form = CreateTopic(request.form)
    if request.method== 'POST':
      if form.validate_on_submit(): #validate form
        try:
          #add topic to database
          new_topic = QuizDatabase(form.topic_name.data, form.topic_description.data)
          db.session.add(new_topic)
          db.session.commit()
          flash('Congratulations! Topic Created!', 'success')
          return redirect(url_for('quiz_view_topics'))#should add a flash saying question submitted for approval
        except exc.IntegrityError:
          db.session.rollback()
          flash("Topic already exists!")
      else:
        return render_template("quiz_topics_creation.html",message = current_user.firstname, form=form)
    else:
      return render_template("quiz_topics_creation.html",message = current_user.firstname, form=form)


@app.route('/quiz/create/<topic>/questions', methods=['POST','GET'])
@login_required
def quiz_questions_creation(topic):
  form = QuestionForm(request.form)
  if request.method== 'POST':
    if form.validate_on_submit():
      #query database for what is topic ID
      try:
        topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first().topic_ID #query what is topic ID for this topic
        new_question=QuizTopic(topic_ID,form.question.data, form.opta.data, form.optb.data, form.optc.data, form.optd.data, form.answer.data) #insert question into database
        db.session.add(new_question)
        db.session.commit()
        flash("Question submitted for approval for topic: "+ topic)
        return redirect(url_for('quiz_view_topics'))#should add a flash saying question submitted for approval
      except exc.IntegrityError:
        db.session.rollback()
        return render_template("error_page.html", error ="Could not submit review")
    else:#not validated, show form again with flash messages
      return render_template("makeQuestion.html", message =  current_user.firstname, topic=topic, form=form)
  else:#if not post, it is just filling in the form
    return render_template("makeQuestion.html", message =  current_user.firstname, topic=topic, form=form)


@app.route('/quiz/take')
@app.route('/quiz/take/<int:page>')
@login_required
def quiz_topics_taking(page=1):
  topics = QuizDatabase.query.filter_by(topic_approved=True).all()
  topics2 = QuizDatabase.query.filter_by(topic_approved=True).order_by(QuizDatabase.topic_Name).paginate(page,5,False)
  available_topics = []
  for topic in topics:
    if topic.topic_approved == True:
      available_topics = topic
  return render_template("quiz_topics_taking.html",message =current_user.firstname, topics=topics2)


@app.route('/quiz/take/<topic>/questions', methods=['POST','GET'])
@login_required
def take_quiz(topic):
  n=5 #number of questions
  form = QuizForm()
  form2 = RateQuizForm()
  topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first() #query what is topic ID for this topic
  if topic_ID == None:
    return render_template("error_page.html", error ="No questions for this topic yet")
  else:
    topic_ID=topic_ID.topic_ID

  qs = QuizTopic.query.filter_by(topic_ID=topic_ID).filter_by(ques_Status="approved").order_by(func.random()).limit(n).all()
  while len(form.questions) < len(qs):
    form.questions.append_entry()
  index = 0
  for question in form.questions:
      question.bart.choices = [('A', qs[index].optA), ('B',qs[index].optB), ('C', qs[index].optC), ('D', qs[index].optD)]
      question.bart.label.text = qs[index].ques
      question.ques_ID = qs[index].ques_ID
      question.bart.default = 'A' #this line didn't work so I changed it in forms as well
      index = index + 1

  if request.method== 'POST':
    if form.validate_on_submit():
      print("Validated")
      score = 0
      for question in form.questions:
        q = QuizTopic.query.filter_by(ques_ID=question.ques_ID).first()
        if q.answer == question.bart.data:
          score = score + 1
      ret = str(score) + "/" + str(len(form.questions))
    #   try:
      topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first().topic_ID
      test = TestRecord(current_user.userID, topic_ID, datetime.datetime.now().date(), score)
      db.session.add(test)
      db.session.commit()
      print("Test Saved")
    #   except:
    #       db.session.rollback()
    #       print(err)
      return render_template("score.html", score=ret,  topic=topic, form2=form2)
    else:
      return render_template("questions.html", form=form, score=None)
  return render_template("questions.html", form=form, score=None)

@app.route('/quiz/rate/<topic>', methods=['POST'])
@login_required
def rate_quiz(topic):
  form= RateQuizForm()
  upVote=0
  downVote=0
  user_comment=form.comment.data
  if request.method == 'POST':
      if form.validate_on_submit():
        if '1' == form.rating.data:
          upVote = upVote+1;
        else:
          downVote = downVote+1
        try:
          topic_ID=QuizDatabase.query.filter_by(topic_Name=topic).first().topic_ID #query what is topic ID for this topic
          new_feedback= Feedback(topic_ID,current_user.userID,user_comment,upVote,downVote)
          db.session.add(new_feedback)
          update_topic = QuizDatabase.query.filter_by(topic_Name=topic).first()
          update_topic.topic_TotalLike = update_topic.topic_TotalLike + upVote;
          update_topic.topic_TotalDislike = update_topic.topic_TotalDislike + downVote;
          #Retrieve all the comments on the topic
          comments=Feedback.query.filter_by(topic_ID=topic_ID).all()
          db.session.commit()

          return render_template("rating.html", comments=comments)
        except exc.IntegrityError:
          db.session.rollback()
          return render_template("error_page.html", error ="Could not submit review")
      else:
        return render_template("error_page.html", error ="No rating detected")
@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
  if current_user.is_authenticated:

    user = User.query.filter_by(email = current_user.email).first()
    test_ID = TestRecord.query.filter_by(userID=current_user.userID).all()
    # test_name = QuizDatabase.query.filter_by(topic_ID=test_ID).first()
    #testRec = TestRecord.query.filter_by(test_ID = current_user.userID).all()
    if test_ID != None:
      for test in test_ID:
        new = str(test.test_Date)
        test.test_Date = new[:11]
    form = PhotoForm()
    if form.validate_on_submit():
      f = form.photo.data
      filename = secure_filename(form.photo.data.filename)
      #Remove old Profile picture
      if user.Dp_filename != None:
        os.remove(app.config['UPLOADED_PHOTOS_DEST'] +'/' + user.Dp_filename)
      form.photo.data.save(app.config['UPLOADED_PHOTOS_DEST'] +'/' + "[" + str(user.userID) + "]" + filename)
      user.Dp_filename = "[" + str(user.userID) + "]" + filename
      db.session.commit()
      return redirect(url_for('account'))
  return render_template("account.html",form=form, message=current_user.firstname,user=user, test_ID = test_ID)

@app.route('/explore/<method>')
@app.route('/explore/<method>/<int:page>')
@login_required
def explore(method, page=1):
  methods = ['topic', 'latest', 'popular']
  #pull questions from database
  #depending on method, show sorted in that order
  if method in methods:
    if method=="latest":
      questions=QuizTopic.query.filter_by(ques_Status="approved").order_by(QuizTopic.ques_ID.desc()).limit(20).all() #only show 20 latest
      questions2=QuizTopic.query.filter_by(ques_Status="approved").order_by(QuizTopic.ques_ID.desc()).paginate(page,5,False)
      print("ENTERIN")
      for question in questions:
        question.topic_Name=QuizDatabase.query.filter_by(topic_ID=question.topic_ID).filter_by(topic_approved=True).first().topic_Name
        question.info="New question added"
        print("HEY")
    if method=="topic":
      return redirect(url_for('quiz_topics_taking'))
    if method=="popular":

      questions = QuizDatabase.query.filter_by(topic_approved=True).order_by(QuizDatabase.topic_TotalLike.desc()).limit(20).all()
      questions2 = QuizDatabase.query.filter_by(topic_approved=True).order_by(QuizDatabase.topic_TotalLike.desc()).paginate(page,5,False)

      for question in questions:
        question.topic_Name=QuizDatabase.query.filter_by(topic_ID=question.topic_ID).first().topic_Name
        if question.topic_TotalLike + question.topic_TotalDislike<1:
            percent = 0;
        else:
          percent = 100.0*question.topic_TotalLike/(question.topic_TotalDislike+question.topic_TotalLike)
        question.info = "Likes: " + str(question.topic_TotalLike) + ", Dislikes: " + str(question.topic_TotalDislike) + ", "+ str(percent) +"%"
      return render_template('explore.html', method=method, message=current_user.firstname, questions=questions2)
    return render_template('explore.html', method=method, message=current_user.firstname, questions=questions2)
  else:
    return render_template("error_page.html", error ="Not a valid method for exploring")

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
  form = SearchForm()
  if request.method == 'POST':
    #if form.validate_on_submit():
    query=request.form['search']
    if query is not None:
     return redirect(url_for('search_results', query=query))
  flash("Search not possible",'Info')
  return render_template('user.html', form = SearchForm())

@app.route('/search_results/<query>')
@login_required
def search_results(query):
   # results = QuizDatabase.query.whoosh_search(query).all()
  results = QuizDatabase.query.filter(QuizDatabase.topic_Name.contains(query)|QuizDatabase.topic_Desc.contains(query)).all()
  users = User.query.filter(User.firstname.contains(query)|User.lastname.contains(query)).all()

  if len(results) == 0:
    flash("Search entry did not match any record!")
  return render_template('search_result.html', query=query, results=results, users=users)

@app.route('/search_results/<query>/<method>')
@app.route('/search_results/<query>/<method>/<int:page>')
@login_required
def search_results_topic(query,  method, page=1,):
  if method == "topics":
    results = QuizDatabase.query.filter(QuizDatabase.topic_Name.contains(query)|QuizDatabase.topic_Desc.contains(query)).order_by(QuizDatabase.topic_Name).paginate(page,5,False)
    return render_template('search_results_topic.html', query=query, results=results, method=method)
  elif method == "users":
    results = User.query.filter(User.firstname.contains(query)|User.lastname.contains(query)).order_by(User.firstname, User.lastname).paginate(page,5,False)
    return render_template('search_results_topic.html', query=query, results=results, method=method)
  return render_template("error_page.html", error ="Search needs to be for either users or quizzes")

@app.route('/users')
@app.route('/users/<int:page>')
@login_required
def show_users(page=1):
  users = User.query.filter_by(role='user').order_by(User.firstname).paginate(page,5,False)
  return render_template('users.html', users=users)

@app.route('/user/<name>.<user_id>')
@login_required
def show_user(name, user_id):
  user = User.query.filter_by(userID = user_id).first()
  print(user.firstname)
  return render_template('show_user.html', user=user)
