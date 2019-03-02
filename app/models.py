from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Users(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Property(db.Model):
    """
    Create a Property table
    """

    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(60), unique=True)


    def __repr__(self):
        return '<Property: {}>'.format(self.name)

class Company(db.Model):
    """
        Create a Company Table
    """
    __tablename__ = 'company'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)

class CompanyHasProperty(db.Model):
    """
        Relation between company and Property
    """

    __tablename__ = 'companyHasproperty'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_id = db.Column(db.INTEGER, db.ForeignKey('company.id'), nullable=False)
    p_id = db.Column(db.INTEGER, db.ForeignKey('property.id'), nullable=False)
