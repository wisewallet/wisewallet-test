from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user
from flask import jsonify

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Users, Company_login, Company, Property, CompanyHasProperty
from ..utils.emails import MailAPI

import datetime
import base64
import json


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an users to the database through the registration form
    """
    if request.method == 'POST':
        data = request.get_json()
        email = data['email'].strip()
        password = data['password']
        username = data['username'].strip()
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        user = Users(email=email,
                     username=username,
                     first_name=first_name,
                     last_name=last_name,
                     password=password
                     )
        try:
            db.session.add(user)
            db.session.commit()
            mail_api = MailAPI()
            msg = "New Registeration\nEmail = "+email+"\t Full name = " \
                + first_name + " " + last_name + "Has just signup."
            mail_api.sendemail(msg)

            response = jsonify(
                {
                    "data": {
                        "code": 200,
                        "message": 'You have successfully registered! You may now login.'
                    }
                }
            )
        except:
            response = jsonify(
                {
                    "data": {
                        "code": 400,
                        "message": "Email or UserName is exist"
                    }
                }
            )
        return response


@auth.route('/company_users/register', methods=['GET', 'POST'])
def company_register():
    if request.method == "POST":
        data = request.get_json()
        email = data['email'].strip()
        password = data['password']
        address_line_1 = data['address_line_1'].strip()
        address_line_2 = data['address_line_2'].strip()
        city = data['city'].strip()
        state = data['state'].strip()
        country = data['country'].strip()
        company_name = data['company_name'].strip()
        zip_code = data['zip_code'].strip()
        category = data["category"].strip()
        causes = data['causes']
        link = data['link'].strip()
        logo = data['logo']
        logo = base64.b64decode(logo)

        company = Company(name=company_name,
                          category=category,
                          link=link,
                          logo=logo,
                          address_line_1=address_line_1,
                          address_line_2=address_line_2,
                          country=country,
                          state=state,
                          city=city,
                          zip_code=zip_code
                          )
        try:
            # add company to the database

            db.session.add(company)
            db.session.commit()
            company = Company.query.filter(
                Company.name == company_name).first()
            company_user = Company_login(
                email=email, password=password, c_id=company.id)
            db.session.add(company_user)
            db.session.commit()
            for name in causes:
                property = Property.query.filter(Property.name == name).first()
                companyHasproperty = CompanyHasProperty(
                    c_id=company.id, p_id=property.id)
                db.session.add(companyHasproperty)
                db.session.commit()
            response = jsonify({'data':
                                {
                                    'code': 200,
                                    'message': 'You have successfully added a new Company.'
                                }
                                })
            return response
        except Exception as e:
            # in case Company name already exists
            print(e)
            response = jsonify({'data':
                                {
                                    'code': 400,
                                    'message': 'company name already exists..'
                                }
                                })
            return response


@auth.route('/company_users/login', methods=['GET', 'POST'])
def company_login():
    """
    Handle requests to the /company_users/login route
    Log an employee in through the login form
    """
    if request.method == 'POST':
        data = request.get_json()
        email = data['email'].strip()
        password = data['password']
        user = Company_login.query.filter_by(email=email).first()
        if user is not None and user.verify_password(
                password):
            data = {}
            final_Data = []
            login_user(user)

            company_details = Company.query.filter(
                Company.id == user.c_id).first()

            data = company_details.get_json()
            data['email'] = user.email
            data['user_id'] = user.id
            data['isCompany'] = user.is_company
            final_Data.append(data)
            response = jsonify({
                'data':
                {
                    "code": 200,
                    "company_user_data": data,
                }
            })
            return response
        # when login details are incorrect
        else:
            response = jsonify({'data':
                                {
                                    'code': 400,
                                    'message': 'Invalid email or password'
                                }
                                })
            return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    if request.method == 'POST':
        data = request.get_json()
        email = data['email'].strip()
        password = data['password']
        user = Users.query.filter_by(email=email).first()
        if user is not None and user.verify_password(
                password):
            login_user(user)
            data = {}
            final_Data = []
            user.remote_address = request.environ.get('HTTP_X_FORWARDED_FOR')
            db.session.add(user)
            db.session.commit()
            if user.is_admin:
                data['user_id'] = user.id
                data['isAdmin'] = user.is_admin
                data['username'] = user.username
                data['email'] = user.email
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                final_Data.append(data)
                response = jsonify({
                    'data':
                    {
                        "code": 200,
                        "userdata": data
                    }
                })
                return response
            else:
                data['user_id'] = user.id
                data['isAdmin'] = user.is_admin
                data['username'] = user.username
                data['email'] = user.email
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                final_Data.append(data)
                response = jsonify({
                    'data':
                    {
                        "code": 200,
                        "userdata": data
                    }
                })
                return response
        # when login details are incorrect
        else:
            response = jsonify({'data':
                                {
                                    'code': 400,
                                    'message': 'Invalid email or password'
                                }
                                })
            return response


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    response = jsonify({'data':
                        {
                            'code': 200,
                            'message': 'You have successfully been logged out.'
                        }
                        })
    return response
