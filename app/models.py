import datetime
import json
import base64

from flask_login import UserMixin
from sqlalchemy import Column, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



class Users(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, nullable=False, unique=True)
    username = db.Column(db.String(60), index=True,
                         nullable=False, unique=True)
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    remote_address = db.Column(db.String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

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
    user = Users.query.get(int(user_id))
    if user:
        return user
    return Company_login.query.get(int(user_id))


class Property(db.Model):
    """
    Create a Property table
    """

    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), index=True, unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Property: {}>'.format(self.name)


class Company_login(UserMixin, db.Model):
    """
        Company users
    """
    __tablename__ = 'company_login'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    c_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    is_company = db.Column(db.Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

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



class Company(db.Model):
    """
        Create a Company Table
    """
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), index=True, unique=True, nullable=False)
    category = db.Column(db.String(256), index=True, nullable=False)
    link = db.Column(db.String(256), unique=True)
    logo = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)
    address_line_1 = db.Column(db.String(256))
    address_line_2 = db.Column(db.String(256))
    city = db.Column(db.String(256))
    state = db.Column(db.String(256))
    country = db.Column(db.String(256))
    zip_code = db.Column(db.String(10))    
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)
    
    def get_json(self):
        import copy
        data = copy.deepcopy(self.__dict__)

        del data["id"]
        del data["created_date"]
        del data["_sa_instance_state"]
        if self.logo or self.logo!="":
            data['logo'] = base64.b64encode(self.logo).decode('ascii')
        else:
            data['logo'] = ""
        return data


class CompanyHasProperty(db.Model):
    """
        Relation between company and Property
    """

    __tablename__ = 'companyHasproperty'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
