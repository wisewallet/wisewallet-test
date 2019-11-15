from flask import render_template
from flask_login import current_user, login_required
from forms import SearchForm
from ..models import Property, Company, CompanyHasProperty
from flask import flash, render_template, request, redirect
from . import home
from flask import jsonify
from sqlalchemy.orm import load_only
from .. import db
from ..utils.search_functions import *

import base64


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    # form = SearchForm()
    company = Company.query.order_by(Company.id).all()
    property = Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    com_dict = {}
    final_Data = []
    for com in company:
        data = {}
        companyHasproperty = CompanyHasProperty.query.with_entities(
            CompanyHasProperty.p_id).filter(
                CompanyHasProperty.c_id == com.id).all()
        companyHasproperty_pid = [value for value, in companyHasproperty]
        company_pid_list = companyHasproperty_pid
        company_pname_list = []
        for id in company_pid_list:
            property = Property.query.filter(Property.id == id).first()
            company_pname_list.append(property.name)
        #com_dict[com.name] = company_pname_list
        data['company_id'] = com.id
        data['company_name'] = com.name
        data['company_category'] = [com.category]
        data['company_link'] = com.link
        data['company_cause'] = company_pname_list
        if com.logo:
            data['company_logo'] = base64.b64encode(com.logo).decode('ascii')
        else:
            data['company_logo'] = ""
        final_Data.append(data)

    response = jsonify({"data":
                        {
                            "code": 200,
                            "company_data": final_Data
                        }
                        })
    return response


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abor(403)
    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/company/<company_name>', methods=['GET', 'POST'])
@login_required
def get_companies_by_name(company_name):
    
    company = Company.query.filter(Company.name == company_name).first()
    companyHasproperty = CompanyHasProperty.query.with_entities(
        CompanyHasProperty.p_id).filter(
            CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]
    property = Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []
    final_Data = []
    data = {}
    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)
    data['company_id'] = company.id
    data['company_name'] = company.name
    data['company_category'] = [company.category]
    data['company_link'] = company.link
    data['company_cause'] = company_pname_list
    if company.logo:
        data['company_logo'] = base64.b64encode(company.logo).decode('ascii')
    else:
        data['company_logo'] = ""

    final_Data.append(data)
    new_data = {}
    new_data = company.get_json()
    new_data['company_cause'] = company_pname_list
    response = jsonify({"data":
                        {
                            "code": 200,
                            "company_data": final_Data,
                            "company_data_display": new_data
                        }
                        })
    return response


@home.route('/property', methods=['GET'])
def get_property_data():
    final_Data = []
    property = Property.query.order_by(Property.id).all()
    for pro in property:
        data = {}
        data['property_id'] = pro.id
        data['property_name'] = pro.name
        final_Data.append(data)
    response = jsonify({"data":
                        {
                            "code": 200,
                            "property_data": final_Data
                        }
                        })
    return response


@home.route('/category', methods=['GET'])
def get_category_data():
    final_data = []
    category = db.session.query(
        Company.category).distinct().order_by(Company.category).all()
    final_data = [value[0] for value in category]
    response = jsonify({"data":
                        {
                            "code": 200,
                            "category_data": final_data
                        }
                        })
    return response


@home.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    data = request.get_json()
    print(data)
    search_company_name = data['search_company_name']
    search_company_category = data['search_company_category']
    search_company_causes = data['search_company_causes']
    print(search_by_company_category)
    print(search_by_company_cause)
    final_Data = search_company_based_on_filters(
        search_company_name,
        search_company_category,
        search_company_causes
    )
    response = jsonify({"data":
                        {
                            "code": 200,
                            "company_data": final_Data
                        }
                        })
    return response
