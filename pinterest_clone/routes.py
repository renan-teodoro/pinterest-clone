from flask import render_template, url_for, redirect, request
from pinterest_clone import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from pinterest_clone.forms import LoginForm, RegistrationForm
from pinterest_clone.models import User, Post


@app.route("/", methods=["GET", "POST"])
def home():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user)
            return redirect(url_for("profile", username=user.username))
    return render_template("home.html", form=loginForm)


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(registrationForm.password.data)
        user = User(
            username=registrationForm.username.data,
            email=registrationForm.email.data,
            password=hashedPassword,
        )
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)

        return redirect(url_for("profile", username=user.username))
    return render_template("create-account.html", form=registrationForm)


@app.route("/profile/<username>")
@login_required
def profile(username):
    user_profile = User.query.filter_by(username=username).first()
    userId = user_profile.id

    if int(userId) == int(current_user.id):
        return render_template("profile.html", user=current_user)

    if int(userId) != int(current_user.id):
        return render_template("profile.html", user=user_profile)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
