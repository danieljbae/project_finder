import os
import secrets
from PIL import Image

# Flask libraries to
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

# Custom Flask objects
from flaskapp import app, db, bcrypter
# Cusom SQL tables
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers,  ProjectLanguages, ProjectCareers
# Cusom User input Forms
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm


@app.route('/')
@app.route('/home')
def home():
    """ Render Home Page with all Projects found in Projects db table """
    projects = Projects.query.all()
    projects = sorted(projects, key=lambda x: x.creation_timestamp, reverse=True)
    return render_template('home.html', projects=projects)


@app.route('/about')
def about():
    """ Render about page """
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Renders Registration Form and adds new-user to the Users db table """
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        # Create User object (1 row) and to Users table
        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(password=hashed_password,
                         email=form.email.data,
                         first_name=form.firstname.data,
                         last_name=form.lastname.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.firstname.data} {form.lastname.data}!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Renders login form, and sets current_user session (based on login info) """

    form = LoginForm()
    # If already logged in, redirect tp
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Validate login credentials with database
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
    """ Shuts down current_user session """

    flash(f"Successfully Logged out {current_user.first_name}!", category='success')
    logout_user()
    return redirect(url_for('home'))


def save_picture_helper(form_picture):
    """ Helper funtion to: Resize/save images in project directory """

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
    """ Views current sessions's user Account and Updates in User db table """
    form = UpdateAccountForm()
    # POST User Account data (view)
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
    # GET User Account data (view)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name

    image_file = url_for('static', filename=f'/profile_pics/{current_user.profile_image}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/projects/new", methods=['GET', 'POST'])
@login_required
def new_project():
    """ Renders Project form and adds to Projects db table """
    form = ProjectForm()
    if form.validate_on_submit() and request.method == 'POST':
        new_project = Projects(name=form.title.data, desc=form.content.data, owner=current_user)
        db.session.add(new_project)
        db.session.commit()
        # Setting values for record in Project table
        for language in form.languages.data:
            project_language = Languages.query.filter_by(id=language).first()
            new_project.languages.append(project_language)
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
    """" Updates project from Projects db table """

    # Current user muster be owner of project to update
    current_project = Projects.query.get_or_404(project_id)
    if current_user != current_project.owner:
        abort(403)

    form = ProjectForm()
    # POST project by project ID
    if form.validate_on_submit() and request.method == 'POST':
        current_project.name = form.title.data
        current_project.desc = form.content.data
        current_project.languages = current_project.careers = []  # Reset exising skills, so new inputs override existing
        db.session.commit()
        # Setting values for record in Project table
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
    # GET project by project ID
    elif request.method == 'GET':
        form.title.data = current_project.name
        form.content.data = current_project.desc

    return render_template('create_project.html', title='Update Project', form=form, legend='Update Project')


@app.route("/projects/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    """" Deletes project from Projects db table """
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
    """ Adds current_user as a team member from a project """
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.append(current_user)
    db.session.commit()
    flash('You succesfully joined the project!', 'success')
    return redirect(url_for('project', project_id=project_id))


@app.route("/projects/<int:project_id>/leave", methods=['GET', 'POST'])
@login_required
def leave_project(project_id):
    """ Removes current_user as a team member from a project """
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.remove(current_user)
    db.session.commit()
    flash('You succesfully left the project!', 'success')
    return redirect(url_for('project', project_id=project_id))
