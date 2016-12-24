from flask import render_template
from flask_mail import Message
from threading import Thread
from . import mail
from .. import app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, subject, template, **kwargs):
    msg = Message(app.config['APP_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['APP_MAIL_SENDER'], recipients=recipients)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
