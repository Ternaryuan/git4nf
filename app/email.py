from flask import render_template, current_app
from flask_mail import Message
from threading import Thread
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, subject, template, **kwargs):
    # 必须使用get_current_object,因为要往线程中传递,而current_app是一个代理,需要flask上下文才能获取到
    app = current_app._get_current_object()
    msg = Message(app.config['APP_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['APP_MAIL_SENDER'], recipients=recipients)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
