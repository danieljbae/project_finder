from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    ''' Login manager extension '''
    return Users.query.get(int(user_id))


# Association tables, related to Users and Projects tables
UserProjects = db.Table("userproject",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                        db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True))
UserLanguages = db.Table("userlanguage",
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                         db.Column("language_id", db.Integer, db.ForeignKey("language.id"), primary_key=True))
UserCareers = db.Table("usercareer",
                       db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                       db.Column("career_id", db.Integer, db.ForeignKey("career.id"), primary_key=True))
ProjectLanguages = db.Table("projectlanguage",
                            db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
                            db.Column("language_id", db.Integer, db.ForeignKey("language.id"), primary_key=True))
ProjectCareers = db.Table("projectcareer",
                          db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
                          db.Column("career_id", db.Integer, db.ForeignKey("career.id"), primary_key=True))


class Users(db.Model, UserMixin):
    ''' Users Table: 
    User profile information 

    UserMixin allows "current_user" to inherit:
        - Users table attributes/columns
        - Standard methods (isAuthenticated, isActive, etc.)
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="Portrait_Placeholder.png")
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)
    # relationships to Association table
    languages = db.relationship('Languages', secondary=UserLanguages, lazy='subquery', backref="get_users")
    careers = db.relationship('Careers', secondary=UserCareers, lazy='subquery', backref="get_users")

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"


class Projects(db.Model):
    ''' Projects Table: 
    Group projects that users can either create or join 
    '''
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=False)
    creation_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    target_end_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    # relationships to Association table
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    owner = db.relationship("Users", foreign_keys=owner_id, backref="owned_projects", uselist=False)
    members = db.relationship('Users', secondary=UserProjects, lazy='subquery', backref="get_projects")
    languages = db.relationship('Languages', secondary=ProjectLanguages, lazy='subquery', backref="get_projects")
    careers = db.relationship('Careers', secondary=ProjectCareers, lazy='subquery', backref="get_projects")

    def __repr__(self):
        return f"Project[ID:'{self.id}', Name:'{self.name}'] "


class Languages(db.Model):
    ''' Languages Table:
    Common technical Languages per StackOverflow 2019 survey
    '''
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False, default="wikisnippet")
    image = db.Column(db.String(20), nullable=False, default="language.jpg")

    def __repr__(self):
        return f"Language('{self.name}', '{self.desc}')"


class Careers(db.Model):
    ''' Careers Table:
    Common SWE related Roles per StackOverflow 2019 survey
    '''
    __tablename__ = 'career'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False, default="wikisnippet")
    image = db.Column(db.String(20), nullable=False, default="career.jpg")

    def __repr__(self):
        return f"Career('{self.name}', '{self.desc}')"
