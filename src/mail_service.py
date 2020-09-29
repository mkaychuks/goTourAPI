from threading import Thread

from flask_mail import Message
from werkzeug.exceptions import InternalServerError

from src import app, mail


# async functions for mail send
def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError('[MAIL SERVER] not working')



def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(target=send_async_mail, args=(app, msg)).start()