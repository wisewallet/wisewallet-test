import base64

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask import jsonify

from . import company
from .. import db
from ..models import Property, Company, CompanyHasProperty


def check_company():
    """
    Prevent non-company from accessing the page
    """
    return current_user.is_company


@company.route('/company', methods=['GET', 'POST'])
@login_required
def get_company():
    """
        get company associated with the user
    """

    if not check_company():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response

    company = Company.query.filter(Company.id == current_user.c_id).first()
    data = company.get_json()

    companyHasproperty = CompanyHasProperty.query.with_entities(
        CompanyHasProperty.p_id).filter(
            CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]

    property = Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []
    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)
    data['company_cause'] = []
    data['company_cause'] = company_pname_list
    response = jsonify({"data":
                        {
                            "code": 200,
                            "company_data": data
                        }
                        })
    return response


@company.route('/company/edit', methods=['GET', 'POST'])
@login_required
def edit_company():
    """
    Edit a company
    """
    if not check_company():
        response = jsonify({
            "status_code": 401,
            "messages": "You are not authorized to access this page",
            "code": 401
        })
        return response

    add_company = False

    if request.method == 'POST':

        company = Company.query.get_or_404(current_user.c_id)
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

        data = request.get_json()
        company.address_line_1 = data['address_line_1'].strip()
        company.address_line_2 = data['address_line_2'].strip()
        company.city = data['city'].strip()
        company.state = data['state'].strip()
        company.country = data['country'].strip()
        company.name = data['company_name'].strip()
        company.zip_code = data['zip_code'].strip()
        company.category = data["category"].strip()
        company.link = data['link'].strip()
        logo = data['logo']
        company.logo = base64.b64decode(logo)

        companyHasproperty = CompanyHasProperty.query.filter(
            CompanyHasProperty.c_id == company.id).all()
        for i in companyHasproperty:
            db.session.delete(i)
        db.session.commit()

        property_names = data['causes']
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
    response = jsonify({
        "status_code": 400,
        "messages": "Method not allowed",
        "code": 400
    })
    return response

# TODO: delete the associated company
