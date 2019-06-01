from flask import abort, flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required

from . import admin
from forms import PropertyForm,CompanyForm
from .. import db
from ..models import Property,Company,CompanyHasProperty
from flask import jsonify

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    return current_user.is_admin


# @app.errorhandler(401)
# def unauthorized(error):
#     response = jsonify({'code': 401, 'message': 'You are not authorized to access'})
#     response.status_code = 401
#     return response

# property Views


@admin.route('/property', methods=['GET', 'POST'])
@login_required
def list_property():
    """
    List all property
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response
    final_Data=[]
    property = Property.query.order_by(Property.id).all()
    for pro in property:
        data = {}
        data['property_id'] = pro.id
        data['property_name'] = pro.name
        final_Data.append(data)
    response = jsonify({'data':
        {
            'code':200,
            "property_data":final_Data
        }
    })
    return response
    return render_template('admin/property/properties.html',
                           property=property, title="property")


@admin.route('/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    """
    Add a property to the database
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response

    add_property = True

    if request.method == 'POST':
        data = request.get_json()
        name  = data['name']
        property = Property(name=name)
        try:
            # add property to the database
            db.session.add(property)
            db.session.commit()
            response = jsonify({'data':
                {
                    'code':200,
                    'message':'You have successfully added a new property.'
                }
            })
            return response
            flash('You have successfully added a new property.')
        except:
            # in case property name already exists
            response = jsonify({'data':
                {
                    'code':400,
                    'message':'property name already exists.'
                }
            })
            return response
            flash('Error: property name already exists.')

    # form = PropertyForm()
    # if form.validate_on_submit():
    #     property = Property(name=form.name.data)
    #     try:
    #         # add property to the database
    #         db.session.add(property)
    #         db.session.commit()
    #         return jsonify({'data':
    #             {
    #                 'code':200,
    #                 'message':'You have successfully added a new property.'
    #             }
    #         })
    #         flash('You have successfully added a new property.')
    #     except:
    #         # in case property name already exists
    #         return jsonify({'data':
    #             {
    #                 'code':400,
    #                 'message':'property name already exists.'
    #             }
    #         })
    #         flash('Error: property name already exists.')

        # redirect to property page
        return redirect(url_for('admin.list_property'))

    # load property template
    # return render_template('admin/property/property.html', action="Add",
    #                        add_property=add_property, form=form,
    #                        title="Add Property")


@admin.route('/property/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    """
    Edit a Property
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response

    add_property = False

    property = Property.query.get_or_404(id)

    if request.method == 'POST':
        data = request.get_json()
        property.name = data['name']
        db.session.commit()
        response = jsonify({'data':
            {
                'code':200,
                'message':'You have successfully edited the property.'
            }
        })
        return response
    response = jsonify({'data':
            {
                'code':200,
                'name': property.name
            }
        })
    return response
    #
    #
    # form = PropertyForm(obj=property)
    # if form.validate_on_submit():
    #     property.name = form.name.data
    #     db.session.commit()
    #     return jsonify({'data':
    #         {
    #             'code':200,
    #             'message':'You have successfully edited the property.'
    #         }
    #     })
    #     flash('You have successfully edited the property.')
    #
    #     # redirect to the property page
    #     return redirect(url_for('admin.list_property'))

    # form.name.data = property.name
    return render_template('admin/property/property.html', action="Edit",
                           add_property=add_property, form=form,
                           property=property, title="Edit property")


@admin.route('/property/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_property(id):
    """
    Delete a property from the database
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response
    property = Property.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.p_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(property)
    db.session.commit()
    response = jsonify({'data':
        {
            'code':200,
            'message':'You have successfully deleted the property.'
        }
    })
    return response
    flash('You have successfully deleted the property.')

    # redirect to the property page
    return redirect(url_for('admin.list_property'))

    return render_template(title="Delete property")

# Company views

@admin.route('/company', methods=['GET', 'POST'])
@login_required
def list_company():
    """
    List all company
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response
    final_Data=[]
    company = Company.query.order_by(Company.id).all()
    for com in company:
        data = {}
        data['company_id'] = com.id
        data['company_name'] = com.name
        data['company_category'] = com.category
        data['company_link'] = com.link
        companyHasproperty = CompanyHasProperty.query.with_entities(CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == com.id).all()
        companyHasproperty_pid = [value for value, in companyHasproperty]
        # form = CompanyForm(obj=company)

        property =  Property.query.with_entities(Property.name).all()
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
            "code":200,
            "company_data":final_Data
        }
    })
    return response
    return render_template('admin/company/companies.html',
                           company=company, title="Company Data")



@admin.route('/company/add', methods=['GET', 'POST'])
@login_required
def add_company():
    """
    Add a Company to the database
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response
    add_company = True
    property =  Property.query.with_entities(Property.name).all()

    # form = CompanyForm()

    property_list = [value for value, in property]

    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        category = data['category']
        link = data['link']

        company = Company(name=name, category=category, link=link)
        try:
            # add company to the database
            db.session.add(company)
            db.session.commit()

            # company_property_list = request.form.getlist('company_property')
            company_property_list = data['property_list']
            company = Company.query.filter(Company.name == name).first()

            for name in company_property_list:
                property = Property.query.filter(Property.name == name).first()
                companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
                db.session.add(companyHasproperty)
                db.session.commit()
            response = jsonify({'data':
                {
                    'code':200,
                    'message':'You have successfully added a new Company.'
                }
            })
            return response
            flash('You have successfully added a new Company.')
        except:
            # in case Company name already exists
            response = jsonify({'data':
                {
                    'code':400,
                    'message':'company name already exists..'
                }
            })
            return response
            flash('Error: company name already exists.')


    # if form.validate_on_submit():
    #     company = Company(name=form.name.data,category=form.category.data)
        # try:
        #     # add company to the database
        #     db.session.add(company)
        #     db.session.commit()
        #
        #     company_property_list = request.form.getlist('company_property')
        #     company = Company.query.filter(Company.name == form.name.data ).first()
        #
        #     for name in company_property_list:
        #         property = Property.query.filter(Property.name == name).first()
        #         companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
        #         db.session.add(companyHasproperty)
        #         db.session.commit()
        #     return jsonify({'data':
        #         {
        #             'code':200,
        #             'message':'You have successfully added a new Company.'
        #         }
        #     })
        #     flash('You have successfully added a new Company.')
        # except:
        #     # in case Company name already exists
        #     return jsonify({'data':
        #         {
        #             'code':400,
        #             'message':'company name already exists..'
        #         }
        #     })
        #     flash('Error: company name already exists.')

        # redirect to company page
        # return redirect(url_for('admin.list_company'))
    # else:
        # print (form.errors)
    # load company template
        # return render_template('admin/company/company.html', action="Add",
                           # add_company=add_company, form=form,property_list = property_list,
                           # title="Add Company")


@admin.route('/company/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    """
    Edit a company
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response

    add_company = False

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.with_entities(CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]
    # form = CompanyForm(obj=company)

    property =  Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []

    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)

    if request.method == 'POST':
        data = request.get_json()
        company.name = data['name']
        company.category = data['category']
        company.link = data['link']
        companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.c_id == company.id).all()
        for i in companyHasproperty:
            db.session.delete(i)
        db.session.commit()
        # property_names = request.form.getlist('company_property')
        property_names = data['property_list']
        for name in property_names:
            property = Property.query.filter(Property.name == name).first()
            companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
            db.session.add(companyHasproperty)
            db.session.commit()
        response = jsonify({'data':
            {
                'code':200,
                'message':'You have successfully edited the company.'
            }
        })
        return response
    # if form.validate_on_submit():
        # company.name = form.name.data
        # companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.c_id == company.id).all()
        # for i in companyHasproperty:
        #     db.session.delete(i)
        # db.session.commit()
        # property_names = request.form.getlist('company_property')
        # for name in property_names:
        #     property = Property.query.filter(Property.name == name).first()
        #     companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
        #     db.session.add(companyHasproperty)
        #     db.session.commit()
        # return jsonify({'data':
        #     {
        #         'code':200,
        #         'message':'You have successfully edited the company.'
        #     }
        # })
        # flash('You have successfully edited the company.')
        # redirect to the property page
        # return redirect(url_for('admin.list_company'))

    # form.name.data = company.name
    # form.category.data = company.category
    response = jsonify({'data':
        {
            'code' : 200,
            'name' : company.name,
            'category' : company.category,
            'link' : company.link,
            'property_list' : company_pid_list,
            'property_name' : company_pname_list
        }
    })
    return response
    # return render_template('admin/company/company.html', action="Edit",
    #                        add_company=add_company, form=form,
    #                        company=company,company_pname_list=company_pname_list,
    #                        property_list=property_list,title="Edit Company")


@admin.route('/company/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    """
    Delete a Company from the database
    """
    if not check_admin():
        response = jsonify({
            "status_code":401,
            "messages" :"You are not authorized to access this page",
            "code" :401
        })
        return response

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.c_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(company)
    db.session.commit()
    response = jsonify({'data':
        {
            'code':200,
            'message':'You have successfully deleted the company.'
        }
    })
    return response
    # flash('You have successfully deleted the company.')
    #
    # # redirect to the company page
    # return redirect(url_for('admin.list_company'))
    #
    # return render_template(title="Delete Company")
