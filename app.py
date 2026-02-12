import os
from flask import Flask, redirect, render_template, url_for, request, session
from algorithms.algorithms import binary_search_handler, bubble_sort_handler
from algorithms.searching_sorting_forms import BubbleSortForm, BinarySearchForm
from extensions import db, bcrypt, login_manager, mail
from auth.forms import ChangeUsernameForm, ForgotPasswordEmailForm,SignUpForm, LoginForm, ChangeNameForm, ChangeEmailForm, PasswordValidationForm, ChangePasswordForm, AccountDeletionForm
from auth.auth import reset_handler, sign_up_handler,pasword_reset_email_handler ,password_validation_handler, login_handler, account_deletion_handler, logout_handler, confirmation_handler, name_change_handler, username_change_handler, email_change_handler, password_change_handler
from models.user import User
from models.algorithm import Algorithm
from flask_login import current_user, login_required
from dotenv import load_dotenv
from algorithms.add_algorithm import add_algorithm


app = Flask(__name__)

load_dotenv()

#Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///" + os.path.join(BASE_DIR, "instance", os.getenv("DATABASE_NAME")))
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

#Initialising database, bcrypt, login_manager and mail
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    algorithms = Algorithm.query.all()
    return render_template("dashboard.html", algorithms = algorithms)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_handler()
    session.pop("password_validated", None)

    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        result = login_handler(form)

        if result:
            next_page = request.args.get("next")

            return redirect(next_page or url_for("dashboard"))
    
    session.pop("password_validated", None)


    return render_template('login.html', form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    name_form = ChangeNameForm()
    username_form = ChangeUsernameForm()
    email_form = ChangeEmailForm()
    password_validation_form = PasswordValidationForm()
    change_password_form = ChangePasswordForm()
    account_deletion_form = AccountDeletionForm()

    is_validated = session.get("password_validated", False)
    
    if password_validation_form.validate_on_submit() and not is_validated:
        result = password_validation_handler(password_validation_form)
        if result:
            session["password_validated"] = True
            is_validated = session.get("password_validated", False)
            return result
    
    if account_deletion_form.is_submitted() and is_validated:
        result = account_deletion_handler()
        if result:
            session["password_validated"] = True
            is_validated = session.get("password_validated", False)
            return result

    if change_password_form.is_submitted() and is_validated:
        result = password_change_handler(change_password_form)
        if result:
            session.pop("password_validated", None)
            return result

    if email_form.is_submitted() and is_validated:
        result = email_change_handler(email_form)
        if result:
            session.pop("password_validated", None)
            return result

    if username_form.is_submitted():
        result = username_change_handler(username_form)
        if result:
            return result
    
    if name_form.is_submitted():
        result = name_change_handler(name_form)
        if result:
            return result

    name_form.first_name.data = current_user.first_name
    name_form.last_name.data = current_user.last_name
    username_form.username.data = current_user.username
    return render_template('settings.html', account_deletion_form = account_deletion_form,name_form=name_form, username_form=username_form, email_form = email_form, password_validation_form = password_validation_form, is_validated= is_validated, change_password_form=change_password_form)

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    return render_template("test.html")

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordEmailForm()
    if form.validate_on_submit():
        result = pasword_reset_email_handler(form)

    return render_template("forgot-password.html", form=form)

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return reset_handler(token)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    return confirmation_handler(token)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for("dashboard"))

    form = SignUpForm()

    
    if form.is_submitted():
        result = sign_up_handler(form)
        if result:
            return result    

    return render_template('signup.html', form=form)

@app.route("/algorithms/bubblesort", methods=["GET", "POST"])
@login_required
def bubble_sort():
    form = BubbleSortForm()
    sorted_list = None
    steps = None
    array_steps = None
    compare_indices = None

    if form.is_submitted():
        sorted_list, steps, array_steps, compare_indices = bubble_sort_handler(form)

    return render_template("algorithms/bubble_sort.html", form=form, sorted_list=sorted_list, steps=steps, array_steps=array_steps, compare_indices=compare_indices, enumerate=enumerate)

@app.route("/algorithms/binarysearch", methods=["GET", "POST"])
@login_required
def binary_search():
    form = BinarySearchForm()
    is_found = None
    steps = None
    array_steps = None
    compare_indices = None
    item = None

    if form.is_submitted():
        is_found, steps, array_steps, compare_indices, item = binary_search_handler(form)

    return render_template("algorithms/binary_search.html", form=form, is_found=is_found, steps=steps, array_steps=array_steps, compare_indices=compare_indices, item=item, enumerate=enumerate)

if __name__ =='__main__':
    app.run(debug=True, use_reloader=False)