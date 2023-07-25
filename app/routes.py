from flask import current_app
from flask import Blueprint, render_template, redirect, session, flash, url_for
from .models import db, User, Feedback
from .forms import UserRegistrationForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)
user = Blueprint('user', __name__)
feedback = Blueprint('feedback', __name__)


@main.route('/')
def home_page():
    if "username" in session:
        username = session["username"]
        return redirect(url_for("user.user_profile", username=username))

    return redirect(url_for("user.register"))

# ==================================== User Routes ==========================================


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
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(url_for("user.user_profile", username=new_user.username))

    return render_template('register.html', form=form)


@user.route('/users/<string:username>')
def user_profile(username):
    if "username" not in session or session['username'] != username:
        flash("You must be logged in to view this page!", "warning")
        return redirect(url_for("main.home_page"))
    else:
        user = User.query.get_or_404(username)

        return render_template("user_profile.html", user=user)


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
            return redirect(url_for("user.user_profile", username=user.username))
        else:
            current_app.logger.info('User authentication failed')
            form.username.errors = ['Invalid username/password.']
    else:
        current_app.logger.info('Form not submitted or not validated')

    return render_template('login.html', form=form)


@user.route('/logout', methods=["POST"])
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect(url_for("main.home_page"))


@user.route('/users/<string:username>/delete')
def delete_user(username):
    if "username" not in session or session['username'] != username:
        flash("You must be logged in to view this page!", "warning")
        return redirect(url_for("main.home_page"))
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("Goodbye!", "info")

        return redirect(url_for("main.home_page"))


# ==================================== Feedback Routes ==========================================


@feedback.route('/users/<string:username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """Add feedback for logged in user"""

    if "username" not in session or session['username'] != username:
        flash("You must be logged in to view this page!", "warning")
        return redirect(url_for("main.home_page"))

    form = FeedbackForm()
    if form.is_submitted() and form.validate():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(
            title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for("user.user_profile", username=username))

    return render_template("/feedback/add.html", form=form, username=username)


@feedback.route("/feedback/<int:feedback_id>/update", methods=["GET"])
def get_update_feedback_form(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or session['username'] != feedback.username:
        flash("You do not have permissions to view this page!", "warning")
        return redirect(url_for("main.home_page"))

    form = FeedbackForm()
    form.title.data = feedback.title
    form.content.data = feedback.content

    return render_template("/feedback/update.html", form=form, feedback=feedback)


@feedback.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or session['username'] != feedback.username:
        flash("You do not have permissions to view this page!", "warning")
        return redirect(url_for("main.home_page"))

    form = FeedbackForm()
    if form.is_submitted() and form.validate():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash('Feedback has been updated!', 'success')
        return redirect(url_for("user.user_profile", username=session['username']))

    # In case form validation failed
    return render_template("/feedback/update.html", form=form, feedback=feedback)


@feedback.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or session['username'] != feedback.username:
        flash("You must be the author of the feedback to delete it!", "warning")
        return redirect(url_for("main.home_page"))

    db.session.delete(feedback)
    db.session.commit()

    flash('Feedback has been deleted!', 'success')
    return redirect(url_for("user.user_profile", username=session['username']))
