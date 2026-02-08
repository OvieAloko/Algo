from flask import redirect, request, url_for, flash, render_template
from datetime import date
from models.user import User
from extensions import db, bcrypt
from flask_login import login_user, logout_user, current_user
from services.email_service import EmailService
from auth.forms import ResendForm, ResendResetForm, ChangePasswordForm

email_service = EmailService()

def sign_up_handler(form):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if not form.validate():
        last_error = None
        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
        return None

    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(first_name = form.first_name.data, last_name = form.last_name.data, username = form.username.data, email = form.email.data, password = hashed_password, account_created = date.today(), confirmed=False)
    db.session.add(new_user)
    db.session.commit()

    email_service.send_confirmation_email(new_user)
    flash("Confirmation email sent to your email", "success")

    return redirect(url_for("login"))

def login_handler(form):
    user = User.query.filter_by(email = form.email_or_username.data).first()

    if not user:
        user = User.query.filter_by(username = form.email_or_username.data).first()
    
    if not user:
        flash("Incorrect Credentials", "warning")
        return None

    if not bcrypt.check_password_hash(user.password, form.password.data):
        flash("Incorrect Credentials", "warning")
        return None
    
    if not user.confirmed:
        flash("Confirmation email sent to you.", "success")
        EmailService().send_confirmation_email(user)
        return None

    login_user(user, remember=True)
    return redirect(url_for("dashboard"))

def logout_handler():
    logout_user()

def confirmation_handler(token):
    result = email_service.confirm_token(token)

    if result=="expired":
        form = ResendForm()
        if form.validate_on_submit():
            return resend_handler(form)
        return render_template("confirm-email.html", status = "expired", form=form)
    
    elif not result:
        form = ResendForm()
        if form.validate_on_submit():
            return resend_handler(form)
        return render_template("confirm-email.html", status = "invalid", form=form)
    
    user = User.query.filter_by(email = result).first_or_404()

    if user.confirmed:
        return render_template("confirm-email.html", status="already-confirmed")

    user.confirmed = True

    db.session.commit()

    return render_template("confirm-email.html", status="success")

def reset_handler(token):
    result = email_service.confirm_token(token)


    if result=="expired":
        form = ResendResetForm()
        if form.validate_on_submit():
            return resend_reset_handler(form)
        return render_template("reset.html", status = "expired", form=form)
    
    elif not result:
        form = ResendResetForm()
        if form.validate_on_submit():
            return resend_reset_handler(form)
        return render_template("reset.html", status = "invalid", form=form)
    
    user = User.query.filter_by(email=result).first_or_404()
    form = ChangePasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Password was changed", "success")
        return redirect(url_for("login"))

    if form.is_submitted() and not form.validate():
        last_error = None
        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        if last_error:
            flash(last_error, "warning")

    return render_template("reset.html", status="success", form=form)

    

def resend_handler(form):
    email = form.email.data
    
    user = User.query.filter_by(email = email).first()

    if not user:
        flash("There is no user with that email.", "warning")
        return render_template("confirm-email.html", status="invalid", form=form)


    elif user.confirmed:
        flash("You have already confirmed your email. Please login. ", "info")
        return redirect(url_for("login"))
    
    else:
        email_service.send_confirmation_email(user)

        flash("Confirmation sent", "success")

        return redirect(url_for("login"))

def resend_reset_handler(form):
    email = form.email.data
    
    user = User.query.filter_by(email = email).first()

    if not user:
        flash("There is no user with that email.", "warning")
        return render_template("confirm-email.html", status="invalid", form=form)
    
    else:
        email_service.send_password_reset_email(user)

        flash("Password Reset Sent", "success")

        return redirect(url_for("login"))

def name_change_handler(form):
    if form.submit.data and form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash("Name updated!", "success")
        return redirect(url_for("settings"))

def username_change_handler(form):
       
    if form.submit.data and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("There is already a user with that username", "warning")
        else:
            current_user.username = form.username.data
            db.session.commit()
            flash("Username updated!", "success")
        return redirect(url_for("settings"))

def password_validation_handler(form):

    if not bcrypt.check_password_hash(current_user.password, form.password.data):
        flash("Incorrect Credentials", "warning")
        return None
    
    flash("Successful. Enter your new email.", "success")
    return redirect(url_for("settings"))

def password_change_handler(form):
    if not form.validate_on_submit():
        last_error = None
        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
        return None
    
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    current_user.password = hashed_password
    db.session.commit()
    flash("Password was changed", "success")
    return redirect(url_for("settings"))

def account_deletion_handler():
    db.session.delete(current_user)
    db.session.commit()

    flash("Your account was deleted", "success")
    return redirect(url_for("login"))

def email_change_handler(form):

    if not form.validate_on_submit() or not form.email.data:
        last_error = None
        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
        return None
    
    existing_user = User.query.filter_by(email = form.email.data).first()

    if existing_user:
        flash("That email is already being used", "warning")
        return None
    
    current_user.email = form.email.data
    current_user.confirmed = False
    db.session.commit()

    email_service.send_confirmation_email(current_user)

    flash("Email updated. Please confirm your new email.", "success")
    return redirect(url_for("settings"))

def pasword_reset_email_handler(form):
    user = User.query.filter_by(email = form.email.data).first()

    if not user:
        user = User.query.filter_by(username = form.email.data).first()
    
    if not user:
        flash("No account with that email.", "warning")
        return None
    
    flash("Reset email sent to you.", "success")
    EmailService().send_password_reset_email(user)
    return None