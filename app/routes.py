from flask import Blueprint, render_template, redirect, session, flash, url_for
from .models import db, User
from .forms import UserRegistrationForm, UserLoginForm
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)
user = Blueprint('user', __name__)


@main.route('/')
def home_page():
    return redirect(url_for("user.register"))


@user.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()
    if form.is_submitted() and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('index.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(url_for("user.secret"))

    return render_template('register.html', form=form)


@user.route('/secret')
def secret():
    if "username" not in session:
        flash("You must be logged in to vies this page!", "warning")
        return redirect(url_for("user.login_user"))
    return ("You made it!")


@user.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserLoginForm()
    if form.is_submitted() and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(url_for("user.secret"))
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


# It is best practice to have your log out route be a POST route instead of a GET route
@user.route('/logout', methods=["POST"])
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect(url_for("main.home_page"))
