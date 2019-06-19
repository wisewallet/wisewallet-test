from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app import db, login_manager
from sqlalchemy import Column, Integer, DateTime

# class Usersdatas(db.Model):
#     """
#     Create a Usersdata table to store user activity
#     """
#     __tablename__ = 'usersdatas'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     u_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     _company_data = db.Column(db.String)
#     _property_data = db.Column(db.String)
#     created_date = Column(DateTime, default=datetime.datetime.utcnow)
#     update_data = Column(DateTime, default=datetime.datetime.utcnow)
#
#     @property
#     def company_data(self):
#         return [company_name for company_name in self._company_data.split(';')]
#
#     @company_data.setter
#     def company_data(self, value):
#         self._company_data += ';%s' % value
#
#     @property
#     def property_data(self):
#         return [property_name for property_name in self._property_data.split(';')]
#
#     @property_data.setter
#     def property_data(self, value):
#         self._property_data += ';%s' % value

class Users(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(60), index=True, nullable=False, unique=True)
    username = db.Column(db.String(60), index=True, nullable=False, unique=True)
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    remote_address = db.Column(db.String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_date = Column(DateTime, default=datetime.datetime.utcnow)

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
    name = db.Column(db.String(60), index=True, unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Property: {}>'.format(self.name)

class Company(db.Model):
    """
        Create a Company Table
    """
    __tablename__ = 'company'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(256), index=True, unique=True, nullable=False)
    category = db.Column(db.String(256), index=True, nullable=False)
    link = db.Column(db.String(256), unique=True)
    logo = db.Column(db.LargeBinary, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)

class CompanyHasProperty(db.Model):
    """
        Relation between company and Property
    """

    __tablename__ = 'companyHasproperty'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)