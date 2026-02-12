from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from models.user import User
from email_validator import validate_email, EmailNotValidError

class SignUpForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Last Name"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30), EqualTo('confirm_password', message="Passwords must match")], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Confirm Password"})

    submit = SubmitField("Sign Up")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if not all(c.isalnum() or c == "_" for c in username.data):
            raise ValidationError("Please make sure your username only has letters, numbers and underscores with no spaces.")

        if existing_user_username:
            raise ValidationError("That username already exists please try another one.")
    
    #Come back and and email validator
    def validate_email(self, email):

        new_email = email.data

        try:
            validate_email(new_email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValidationError(str(e))

        existing_user_email = User.query.filter_by(email=new_email).first()

        if existing_user_email:
            raise ValidationError("That email already exists please try another one.")
    
    def validate_password(self,password):
        pwd = password.data     
        if not any(i.isupper() for i in pwd):
            raise ValidationError("Please include a capital letter in your passoword")
        
        if not any(i.isdigit() for i in pwd):
            raise ValidationError("Please ensure your password contains a number")

class LoginForm(FlaskForm):
    email_or_username = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email or Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

class ResendForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Send Verification")

class ResendResetForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Send Verification")

class ChangeNameForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField(validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField("Save Changes")

class ChangeEmailForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Change Email")

    def validate_email(self, email):

        new_email = email.data

        try:
            validate_email(new_email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValidationError(str(e))

        existing_user_email = User.query.filter_by(email=email.data).first()

        if existing_user_email:
            raise ValidationError("That email already exists please try another one.")

class PasswordValidationForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Confirm")

class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30), EqualTo('confirm_password', message="Passwords must match")], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Change Password")

    def validate_password(self,password):
        pwd = password.data     
        if not any(i.isupper() for i in pwd):
            raise ValidationError("Please include a capital letter in your passoword")
        
        if not any(i.isdigit() for i in pwd):
            raise ValidationError("Please ensure your password contains a number")

class AccountDeletionForm(FlaskForm):
    submit = SubmitField("Delete Account")

class ChangeUsernameForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Password"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    submit = SubmitField("Change Username")

    def validate_username(self,username):
        existing_user = User.query.filter_by(username=username.data).first()
        if not all(c.isalnum() or c == "_" for c in username.data):
            raise ValidationError("Please make sure your username only has letters, numbers and underscores with no spaces.")

        if existing_user and existing_user.id != current_user.id:
            raise ValidationError("That username already exists please try another one.")

class ForgotPasswordEmailForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Send Email")
