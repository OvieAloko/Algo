from flask import url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from extensions import mail

class EmailService:
    def generate_token(self, email):
        serialiser = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serialiser.dumps(email, salt='email-confirmation-salt')

    def confirm_token(self, token, expiration=3600):
        serialiser = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serialiser.loads(token, salt='email-confirmation-salt', max_age=expiration)
        except SignatureExpired:
            return "expired"
        except BadSignature:
            return None
        return email
    
    def send_email(self, subject, recipients, body):
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = body
        mail.send(msg)
    
    def send_confirmation_email(self,user):
        token = self.generate_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        body = f"Hi {user.first_name}, please confirm your email by clicking this link: {confirm_url}"
        self.send_email("Confirm your email", [user.email], body)
    
    def send_password_reset_email(self, user):
        token = self.generate_token(user.email)
        reset_url = url_for('reset_password', token=token, _external=True)
        body = f"Hi {user.first_name}, please reset your password by clicking this link: {reset_url}"
        self.send_email("Reset your password", [user.email], body)