from petcare import app, mail
from flask import render_template
from flask_mail import Message

def send_registration_confirmation_mail(email, confirm_url):
    with app.app_context():
        msg = Message(subject="Confirm Registration",
                        sender=f"Petcare Register <{app.config['MAIL_USERNAME']}>",
                        recipients=[email], # replace with your email for testing,
                        html=render_template('user/activate.html', email=email, confirm_url=confirm_url)
                    )
        mail.send(msg)