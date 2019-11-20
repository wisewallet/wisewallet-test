from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from .. import db
from ..models import Property, Company, CompanyHasProperty
from flask import jsonify

import base64


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    return current_user.is_admin


# property Views
@admin.route('/property', methods=['GET', 'POST'])
# @login_required
def list_property():
    """
    List all property
    """
    # if not check_admin():
    #     response = jsonify({
    #         "status_code": 401,
    #         "messages": "You are not authorized to access this page",
    #         "code": 401
    #     })
    #     return response
    final_Data = []
    property = Property.query.order_by(Property.id).all()
    for pro in property:
        data = {}
        data['property_id'] = pro.id
        data['property_name'] = pro.name
        final_Data.append(data)
    response = jsonify({'data':
                        {
                            'code': 200,
                            "property_data": final_Data
                        }
                        })
    return response


@admin.route('/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    """
    Add a property to the database
    """
    if not check_admin():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response

    add_property = True

    if request.method == 'POST':
        data = request.get_json()
        name = data['name'].strip()
        property = Property(name=name)
        try:
            # add property to the database
            db.session.add(property)
            db.session.commit()
            response = jsonify({'data':
                                {
                                    'code': 200,
                                    'message': 'You have successfully added a new property.'
                                }
                                })
            return response
        except:
            # in case property name already exists
            response = jsonify({'data':
                                {
                                    'code': 400,
                                    'message': 'property name already exists.'
                                }
                                })
            return response


@admin.route('/property/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    """
    Edit a Property
    """
    if not check_admin():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response

    add_property = False

    property = Property.query.get_or_404(id)

    if request.method == 'POST':
        data = request.get_json()
        property.name = data['name'].strip()
        db.session.commit()
        response = jsonify({'data':
                            {
                                'code': 200,
                                'message': 'You have successfully edited the property.'
                            }
                            })
        return response
    response = jsonify({'data':
                        {
                            'code': 200,
                            'name': property.name
                        }
                        })
    return response


@admin.route('/property/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_property(id):
    """
    Delete a property from the database
    """
    if not check_admin():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response
    property = Property.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(
        CompanyHasProperty.p_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(property)
    db.session.commit()
    response = jsonify({'data':
                        {
                            'code': 200,
                            'message': 'You have successfully deleted the property.'
                        }
                        })
    return response

# Company views


@admin.route('/company', methods=['GET', 'POST'])
# @login_required
def list_company():
    """
    List all company
    """
    # if not check_admin():
    #     response = jsonify({
    #         "status_code": 401,
    #         "messages": "You are not authorized to access this page",
    #         "code": 401
    #     })
    #     return response
    final_Data = []
    company = Company.query.order_by(Company.id).all()
    for com in company:
        data = {}
        data['company_id'] = com.id
        data['company_name'] = com.name
        data['company_category'] = com.category
        data['company_link'] = com.link
        if com.logo:
            data['company_logo'] = base64.b64encode(com.logo).decode('ascii')
        else:
            data['company_logo'] = ""
        companyHasproperty = CompanyHasProperty.query.with_entities(
            CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == com.id).all()
        companyHasproperty_pid = [value for value, in companyHasproperty]

        property = Property.query.with_entities(Property.name).all()
        property_list = [value for value, in property]
        company_pid_list = companyHasproperty_pid
        company_pname_list = []
        for id in company_pid_list:
            property = Property.query.filter(Property.id == id).first()
            company_pname_list.append(property.name)
        data['company_cause'] = company_pname_list
        final_Data.append(data)
    response = jsonify({"data":
                        {
                            "code": 200,
                            "company_data": final_Data
                        }
                        })
    return response


@admin.route('/company/add', methods=['GET', 'POST'])
@login_required
def add_company():
    """
    Add a Company to the database
    """
    if not check_admin():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response
    add_company = True
    property = Property.query.with_entities(Property.name).all()

    # form = CompanyForm()

    property_list = [value for value, in property]

    if request.method == 'POST':
        data = request.form
        name = data['name'].strip()
        category = data['category'].strip()
        link = data['link'].strip()
        files = request.files.getlist('logo')
        logo = files[0].read()
        company_property_list = request.form.getlist('property_list')
        print(type(logo))
        company = Company(name=name, category=category, link=link, logo=logo)
        print(company)
        try:
            # add company to the database
            db.session.add(company)
            db.session.commit()
            company = Company.query.filter(Company.name == name).first()
            for name in company_property_list:
                property = Property.query.filter(Property.name == name).first()
                companyHasproperty = CompanyHasProperty(
                    c_id=company.id, p_id=property.id)
                db.session.add(companyHasproperty)
                print(name)
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
            response = jsonify({'data':
                                {
                                    'code': 400,
                                    'message': 'company name already exists..'
                                }
                                })
            return response


@admin.route('/company/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    """
    Edit a company
    """
    if not check_admin():
        if not check_company():
            response = jsonify({
                "status_code": 401,
                "messages": "You are not authorized to access this page",
                "code": 401
            })
            return response

    add_company = False

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.with_entities(
        CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]

    property = Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []

    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)

    if request.method == 'POST':
        data = request.form
        company.name = data['name'].strip()
        company.category = data['category'].strip()
        company.link = data['link'].strip()
        files = request.files.getlist('logo')
        if len(files) > 0:
            company.logo = files[0].read()
        company.address_line_1 = data['address_line_1'].strip()
        company.address_line_2 = data['address_line_2'].strip()
        company.city = data['city'].strip()
        company.state = data['state'].strip()
        company.country = data['country'].strip()
        company.zip_code = data['zip_code'].strip()

        companyHasproperty = CompanyHasProperty.query.filter(
            CompanyHasProperty.c_id == company.id).all()
        for i in companyHasproperty:
            db.session.delete(i)
        db.session.commit()
        # property_names = request.form.getlist('company_property')
        property_names = request.form.getlist('property_list')
        for name in property_names:
            property = Property.query.filter(Property.name == name).first()
            companyHasproperty = CompanyHasProperty(
                c_id=company.id, p_id=property.id)
            db.session.add(companyHasproperty)
            db.session.commit()
        response = jsonify({'data':
                            {
                                'code': 200,
                                'message': 'You have successfully edited the company.'
                            }
                            })
        return response

    data = company.get_json()
    data['company_cause'] = []
    data['company_cause'] = company_pname_list
    response = jsonify({'data':
                        {
                            'code': 200,
                            'company_data': data
                        }
                        })
    return response


@admin.route('/company/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    """
    Delete a Company from the database
    """
    if not check_admin():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(
        CompanyHasProperty.c_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(company)
    db.session.commit()
    response = jsonify({'data':
                        {
                            'code': 200,
                            'message': 'You have successfully deleted the company.'
                        }
                        })
    return response
