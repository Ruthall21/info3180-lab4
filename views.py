import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm, UploadForm

### Routes ###

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html', name="Ruth-Ann Allen")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()

        # No hashing needed for Lab 4
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for("upload"))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.photo.data
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])

            # Make sure folder exists
            os.makedirs(upload_path, exist_ok=True)

            file.save(os.path.join(upload_path, filename))
            flash(f'{filename} uploaded successfully!', 'success')
            return redirect(url_for('files'))

    return render_template('upload.html', form=form)


def get_uploaded_images():
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_path):
        return []
    return [f for f in os.listdir(upload_path) if os.path.isfile(os.path.join(upload_path, f))]


@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), filename)


@app.route('/files')
@login_required
def files():
    images = get_uploaded_images()
    return render_template('files.html', images=images)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('home'))