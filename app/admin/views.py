from flask import abort, flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required

from . import admin
from forms import PropertyForm,CompanyForm
from .. import db
from ..models import Property,Company,CompanyHasProperty


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# property Views


@admin.route('/property', methods=['GET', 'POST'])
@login_required
def list_property():
    """
    List all property
    """
    check_admin()

    property = Property.query.order_by(Property.id).all()

    return render_template('admin/property/properties.html',
                           property=property, title="property")


@admin.route('/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    """
    Add a property to the database
    """
    check_admin()

    add_property = True

    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(name=form.name.data)
        try:
            # add property to the database
            db.session.add(property)
            db.session.commit()
            flash('You have successfully added a new property.')
        except:
            # in case property name already exists
            flash('Error: property name already exists.')

        # redirect to property page
        return redirect(url_for('admin.list_property'))

    # load property template
    return render_template('admin/property/property.html', action="Add",
                           add_property=add_property, form=form,
                           title="Add Property")


@admin.route('/property/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    """
    Edit a Property
    """
    check_admin()

    add_property = False

    property = Property.query.get_or_404(id)
    form = PropertyForm(obj=property)
    if form.validate_on_submit():
        property.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the property.')

        # redirect to the property page
        return redirect(url_for('admin.list_property'))

    form.name.data = property.name
    return render_template('admin/property/property.html', action="Edit",
                           add_property=add_property, form=form,
                           property=property, title="Edit property")


@admin.route('/property/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_property(id):
    """
    Delete a property from the database
    """
    check_admin()

    property = Property.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.p_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(property)
    db.session.commit()

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
    check_admin()

    company = Company.query.order_by(Company.id).all()

    return render_template('admin/company/companies.html',
                           company=company, title="Company Data")



@admin.route('/company/add', methods=['GET', 'POST'])
@login_required
def add_company():
    """
    Add a Company to the database
    """
    check_admin()

    add_company = True
    property =  Property.query.with_entities(Property.name).all()

    form = CompanyForm()

    property_list = [value for value, in property]

    if form.validate_on_submit():
        company = Company(name=form.name.data,category=form.category.data)
        try:
            # add company to the database
            db.session.add(company)
            db.session.commit()

            company_property_list = request.form.getlist('company_property')
            company = Company.query.filter(Company.name == form.name.data ).first()

            for name in company_property_list:
                property = Property.query.filter(Property.name == name).first()
                companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
                db.session.add(companyHasproperty)
                db.session.commit()
            flash('You have successfully added a new Company.')
        except:
            # in case Company name already exists
            flash('Error: company name already exists.')

        # redirect to company page
        return redirect(url_for('admin.list_company'))
    else:
        # print (form.errors)
    # load company template
        return render_template('admin/company/company.html', action="Add",
                           add_company=add_company, form=form,property_list = property_list,
                           title="Add Company")


@admin.route('/company/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    """
    Edit a company
    """
    check_admin()

    add_company = False

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.with_entities(CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == company.id).all()
    companyHasproperty_pid = [value for value, in companyHasproperty]
    form = CompanyForm(obj=company)

    property =  Property.query.with_entities(Property.name).all()
    property_list = [value for value, in property]
    company_pid_list = companyHasproperty_pid
    company_pname_list = []
    for id in company_pid_list:
        property = Property.query.filter(Property.id == id).first()
        company_pname_list.append(property.name)

    if form.validate_on_submit():
        company.name = form.name.data
        companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.c_id == company.id).all()
        for i in companyHasproperty:
            db.session.delete(i)
        db.session.commit()
        property_names = request.form.getlist('company_property')
        for name in property_names:
            property = Property.query.filter(Property.name == name).first()
            companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = property.id)
            db.session.add(companyHasproperty)
            db.session.commit()
        flash('You have successfully edited the company.')

        # redirect to the property page
        return redirect(url_for('admin.list_company'))

    form.name.data = company.name
    form.category.data = company.category
    return render_template('admin/company/company.html', action="Edit",
                           add_company=add_company, form=form,
                           company=company,company_pname_list=company_pname_list,
                           property_list=property_list,title="Edit Company")


@admin.route('/company/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    """
    Delete a Company from the database
    """
    check_admin()

    company = Company.query.get_or_404(id)
    companyHasproperty = CompanyHasProperty.query.filter(CompanyHasProperty.c_id == id).all()
    for i in companyHasproperty:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(company)
    db.session.commit()

    flash('You have successfully deleted the company.')

    # redirect to the company page
    return redirect(url_for('admin.list_company'))

    return render_template(title="Delete Company")
