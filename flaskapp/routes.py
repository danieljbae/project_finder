# Make a note about (skelaton)
# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/06-Login-Auth/flaskblog/routes.py

import secrets
import os
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import app, db, bcrypter
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers,  ProjectLanguages, ProjectCareers
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm


@app.route('/')
@app.route('/home')
def home():
    projects = Projects.query.all()
    projects = sorted(projects, key=lambda x: x.creation_timestamp, reverse=True)
    for project in projects:
        print(project.creation_timestamp)
    return render_template('home.html', projects=projects)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Validate user submission, then re-direct to home page 

    Validate:
        - Form fields contstraints
        - Database: Confirm user is not duplicate"""

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(password=hashed_password, email=form.email.data,
                     first_name=form.firstname.data, last_name=form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.firstname.data} {form.lastname.data}!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Valididate User submission, then login current_user, otherwise provide feedback
    - Re-directs users to pages which required login access (next_page)

    Validate:
        - Form field contstraints
        - Database: Confirm user has an account """

    form = LoginForm()
    if current_user.is_authenticated:  # if already logged in
        return redirect(url_for('home'))

    # Validate login fields in database
    if form.validate_on_submit() and request.method == 'POST':
        form_email, form_password = form.email.data, form.password.data
        db_user = Users.query.filter_by(email=form_email).first()
        if db_user and bcrypter.check_password_hash(pw_hash=db_user.password, password=form_password):
            login_user(db_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Successfully logged in. Welcome {db_user.first_name} {db_user.last_name}!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unable to login. Email and password combination does not match/exist', category='danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    flash(f"Successfully Logged out {current_user.first_name}!", category='success')
    logout_user()
    return redirect(url_for('home'))


def save_picture_helper(form_picture):
    ''' helper function which
    1) Takes pictures field (.jpg, .png) submitted on form
    2) Set save location for picures
    3) Resize and save image '''

    # creating unique name when saving pictures
    rand_hex = secrets.token_hex(nbytes=8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = rand_hex + file_ext
    # Setting file path for save location
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    # image resizing and saving
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    ''' User account route '''

    form = UpdateAccountForm()
    if form.validate_on_submit() and request.method == 'POST':
        if form.picture.data:  # Save and Set profile picture
            picture_file = save_picture_helper(form.picture.data)
            current_user.profile_image = picture_file

        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You've successfully updated your account!", category="success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name

    image_file = url_for('static', filename=f'/profile_pics/{current_user.profile_image}')

    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/projects/new", methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit() and request.method == 'POST':
        new_project = Projects(name=form.title.data, desc=form.content.data, owner=current_user)
        db.session.add(new_project)
        db.session.commit()

        # Adding Multiple languages to a project
        for language in form.languages.data:
            project_language = Languages.query.filter_by(id=language).first()
            new_project.languages.append(project_language)

        # Adding Multiple Careers to a project
        for career in form.careers_field.data:
            project_career = Careers.query.filter_by(id=career).first()
            new_project.careers.append(project_career)

        new_project.members.append(current_user)
        db.session.commit()

        flash("Your post has been created successfully!", "success")
        return redirect(url_for('home'))
    return render_template('create_project.html', legend='New Project', form=form)


@app.route("/projects/<int:project_id>")
def project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    return render_template('project.html', title=current_project.name, current_project=current_project)


@app.route("/projects/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    ''' Form for current user to update their project
    current user muster be owner of the posted project, otherwise 403 '''
    current_project = Projects.query.get_or_404(project_id)
    if current_project.owner != current_user:
        abort(403)

    form = ProjectForm()
    if form.validate_on_submit() and request.method == 'POST':
        current_project.name = form.title.data
        current_project.desc = form.content.data

        # Reset exising skills, so User inputs overrides existing values
        current_project.languages = []
        current_project.careers = []
        db.session.commit()

        for language in form.languages.data:
            project_language = Languages.query.filter_by(id=language).first()
            if project_language not in current_project.languages:
                current_project.languages.append(project_language)

        for career in form.careers_field.data:
            project_career = Careers.query.filter_by(id=career).first()
            current_project.careers.append(project_career)
        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('project', project_id=current_project.id))

    elif request.method == 'GET':
        form.title.data = current_project.name
        form.content.data = current_project.desc

    return render_template('create_project.html', title='Update Project', form=form, legend='Update Project')


@app.route("/projects/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    if current_project.owner != current_user:
        abort(403)
    db.session.delete(current_project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/projects/<int:project_id>/join", methods=['GET', 'POST'])
@login_required
def join_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.append(current_user)
    db.session.commit()
    flash('You succesfully joined the project!', 'success')
    return redirect(url_for('project', project_id=project_id))


@app.route("/projects/<int:project_id>/leave", methods=['GET', 'POST'])
@login_required
def leave_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.remove(current_user)
    db.session.commit()
    flash('You succesfully left the project!', 'success')
    return redirect(url_for('project', project_id=project_id))
