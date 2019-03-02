from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import PropertyForm
from .. import db
from ..models import Property


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
    #companyHasproperty = CompanyHasProperty.get_or_404(CompanyHasProperty.id).filter(CompanyHasProperty.p_id == id)
    db.session.delete(property)
    #db.session.delete(companyHasproperty)
    db.session.commit()
    flash('You have successfully deleted the property.')

    # redirect to the property page
    return redirect(url_for('admin.list_property'))

    return render_template(title="Delete property")

#
# @admin.route('/company', methods=['GET', 'POST'])
# @login_required
# def list_company():
#     """
#     List all company
#     """
#     check_admin()
#
#     company = Company.query.all()
#     property = Property.query.all()
#     companyHasproperty = Property.query.join(CompanyHasProperty, property.id== CompanyHasProperty.p_id).filter(CompanyHasProperty.c_id == Company.id)
#
#     return render_template('admin/property/company.html',
#                            company=company,property=property,companyHasproperty = companyHasproperty, title="Company Data")
#
#
# @admin.route('/company/add', methods=['GET', 'POST'])
# @login_required
# def add_company():
#     """
#     Add a property to the database
#     """
#     check_admin()
#
#     add_company = True
#
#     form = CompanyForm()
#     companyhaspropertyform = CompanyHasPropertyForm()
#     page_ids = request.companyhaspropertyform.get("property-list")
#     print(page_ids)
#     if form.validate_on_submit():
#         company = Company(name=form.name.data,category=form.category.data)
#
#         try:
#             # add company to the database
#             db.session.add(company)
#             db.session.commit()
#             company = Company.query.filter_by(name=form.name.data).first()
#             for i in page_ids:
#                 companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = i)
#                 db.session.add(companyHasproperty)
#                 db.session.commit()
#             flash('You have successfully added a new Company.')
#         except:
#             # in case Company name already exists
#             flash('Error: company name already exists.')
#
#         # redirect to company page
#         return redirect(url_for('admin.list_company'))
#
#     # load company template
#     return render_template('admin/property/company.html', action="Add",
#                            add_company=add_company, form=form,
#                            title="Add Company")
#
#
# @admin.route('/company/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_company(id):
#     """
#     Edit a company
#     """
#     check_admin()
#
#     add_company = False
#
#     company = Company.query.get_or_404(id)
#     companyHasproperty = CompanyHasProperty.query.filter_by(c_id = company.id).all()
#     form = CompanyForm(obj=company)
#     companyhaspropertyform = CompanyHasPropertyForm(obj=companyHasproperty)
#     if form.validate_on_submit():
#         company.name = form.name.data
#         page_ids = companyhaspropertyform.get('property-list')
#         for i in page_ids:
#             companyHasproperty = CompanyHasProperty(c_id = company.id,p_id = i)
#             db.session.commit()
#         db.session.commit()
#         flash('You have successfully edited the property.')
#
#         # redirect to the property page
#         return redirect(url_for('admin.list_property'))
#
#     form.name.data = company.name
#     companyHaspropertyform.getlist.data =
#     return render_template('admin/property/property.html', action="Edit",
#                            add_property=add_property, form=form,
#                            property=property, title="Edit property")
#
#
# @admin.route('/property/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_property(id):
#     """
#     Delete a property from the database
#     """
#     check_admin()
#
#     property = Property.query.get_or_404(id)
#     companyHasproperty = CompanyHasProperty.get_or_404(CompanyHasProperty.id).filter(CompanyHasProperty.p_id == id)
#     db.session.delete(property)
#     db.session.delete(companyHasproperty)
#     db.session.commit()
#     flash('You have successfully deleted the property.')
#
#     # redirect to the property page
#     return redirect(url_for('admin.list_property'))
#
#     return render_template(title="Delete property")
