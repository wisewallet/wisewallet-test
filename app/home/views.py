from flask import render_template
from flask_login import current_user,login_required
from forms import SearchForm
from ..models import Property,Company,CompanyHasProperty
from flask import flash, render_template, request, redirect
from . import home
from flask import jsonify


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    # form = SearchForm()
    company = Company.query.order_by(Company.id).all()
    property =  Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    com_dict = {}
    data = {}
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
        data['company_link'] = comp.link
        data['company_cause'] = company_pname_list
        final_Data.append(data)

    response = jsonify({"data":
        {
            "code":200,
            "company_data":final_Data
        }
    })
    return response
    # return render_template('home/dashboard.html',form=form, company=company,
    #                         property_list=property_list,
    #                         company_pname_list=company_pname_list,
    #                         com_dict=com_dict,
    #                         title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abor(403)
    return render_template('home/admin_dashboard.html',title="Dashboard")

@home.route('/company/<company_name>',methods=['GET','POST'])
@login_required
def get_companies_by_name(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    companyHasproperty = CompanyHasProperty.query.with_entities(
        CompanyHasProperty.p_id).filter(
            CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]
    property =  Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []
    final_Data = []
    data = {}
    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)
    data['company_id'] = com.id
    data['company_name'] = com.name
    data['company_category'] = [com.category]
    data['company_link'] = com.link
    data['company_cause'] = company_pname_list
    final_Data.append(data)
    response = jsonify({"data":
        {
            "code":200,
            "company_data":final_Data
        }
    })
    return response
    # return render_template('home/companies.html',company=company,
    #                         company_pname_list=company_pname_list,
    #                         property_list=property_list,title=company.name)

@home.route('/search',methods=['GET', 'POST'])
@login_required
def search():
    # form = SearchForm()
    data = request.get_json()
    search = data['search']
    company = Company.query.filter(Company.name.like('%' + search + '%'))
    property =  Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    com_dict = {}
    data = {}
    final_Data = []
    for com in company:
        companyHasproperty = CompanyHasProperty.query.with_entities(
            CompanyHasProperty.p_id).filter(
                CompanyHasProperty.c_id == com.id).all()
        companyHasproperty_pid = [value for value, in companyHasproperty]
        company_pid_list = companyHasproperty_pid
        company_pname_list = []
        for id in company_pid_list:
            property = Property.query.filter(Property.id == id).first()
            company_pname_list.append(property.name)
        com_dict[com.name] = company_pname_list
        data = {}
        data['company_id'] = com.id
        data['company_name'] = com.name
        data['company_category'] = [com.category]
        data['company_link'] = com.link
        data['company_cause'] = company_pname_list
        final_Data.append(data)
    response = jsonify({"data":
        {
            "code":200,
            "company_data":final_Data
        }
    })
    return response
    # return render_template('home/dashboard.html',form=form, company=company,
    #                         property_list=property_list,
    #                         com_dict=com_dict,
    #                         title="Dashboard")
