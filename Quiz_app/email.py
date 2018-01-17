from . import app, mail
from flask import url_for, render_template
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html):
    msg = Message(subject, recipients=[recipients])
    msg.html = html
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr

def send_confirmation_email(new_user):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    confirm_url = url_for(
        'confirm_email',
        token=confirm_serializer.dumps(new_user.email, salt='too-salt-for-confirmation'),
        _external=True)
 
    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url, user=new_user.firstname)
 
    send_email('Confirm Your Email Address', new_user.email, html)

def password_reset_email(user):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    password_reset_url = url_for(
        'reset_password_email',
        token=confirm_serializer.dumps(user.email, salt='too-too-too-salty-for-confirmation'),
        _external=True)
 
    html = render_template(
        'password_reset_email.html',
        password_reset_url=password_reset_url, user=user.firstname)
 
    send_email('Password Reset For Peer Quiz Account', user.email, html)