from flask import flash, redirect, render_template, url_for,request
from flask_login import login_required, login_user, logout_user
from flask import jsonify

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Users
from ..utils.emails import MailAPI

import datetime

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an users to the database through the registration form
    """
    if request.method=='POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        user = Users(email=email,
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            password=password)
                            # create_date=datetime.datetime.utcnow,
                            # updated_date=None)
        try:
            db.session.add(user)
            db.session.commit()
            mail_api = MailAPI()
            # mail_api.send_simple_message(to_email = "vmehta342@gmail.com")
            msg = "New Registeration\nEmail = "+email+"\t Full name = " \
                + first_name + " " + last_name + "Has just signup."
            mail_api.sendemail(msg)
        #mail_api.send_simple_message(content=msg)
            response = jsonify(
                {
                    "data":{
                        "code":200,
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
        # flash('You have successfully registered! You may now login.')

        # return redirect(url_for('auth.login'))

    # load registration template
    # return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    if request.method=='POST':
        data = request.get_json()
        email = data['email']
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
                        "code":200,
                        "userdata":data
                    }
                        })

                return response
                return redirect(url_for('home.admin_dashboard'))
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
                        "code":200,
                        "userdata":data
                    }
                        })
                return response
                return redirect(url_for('home.dashboard'))
        # when login details are incorrect
        else:
            response = jsonify({'data':
                {
                    'code':400,
                    'message':'Invalid email or password'
                }
            })
            return response
    #form = LoginForm()
    # if form.validate_on_submit():
    #
    #     # check whether employee exists in the database and whether
    #     # the password entered matches the password in the database
    #     user = Users.query.filter_by(email=form.email.data).first()
    #     if user is not None and user.verify_password(
    #             form.password.data):
    #         # log employee in
    #         login_user(user)
    #         data = {}
    #         final_Data = []
    #         if user.is_admin:
    #             data['user_id'] = user.id
    #             data['isAdmin'] = user.is_admin
    #             data['username'] = user.username
    #             data['email'] = user.email
    #             final_Data.append(data)
    #             return jsonify({
    #                 'data':
    #                 {
    #                     "code":200,
    #                     "userdata":data
    #                 }
    #                     })
    #             return redirect(url_for('home.admin_dashboard'))
    #         else:
    #             data['user_id'] = user.id
    #             data['isAdmin'] = user.is_admin
    #             data['username'] = user.username
    #             data['email'] = user.email
    #             final_Data.append(data)
    #             return jsonify({
    #                 'data':
    #                 {
    #                     "code":200,
    #                     "userdata":data
    #                 }
    #                     })
    #             return redirect(url_for('home.dashboard'))
    #
    #
    #     # when login details are incorrect
    #     else:
    #         return jsonify({'data':
    #             {
    #                 'code':400,
    #                 'message':'Invalid email or password'
    #             }
    #         })
    #         flash('Invalid email or password.')

    # load login template
    # return render_template('auth/login.html', form=form, title='Login')


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
            'code':200,
            'message': 'You have successfully been logged out.'
        }
    })
    return response
    # flash('You have successfully been logged out.')

    # redirect to the login page
    # return redirect(url_for('auth.login'))
