from ..models import Property,Company,CompanyHasProperty
import base64

def search_by_company_name(search=None):
    if search is None:
        return "Not found"
    company_id = []
    company = Company.query.with_entities(
            Company.id).filter(Company.name.like('%' + search + '%')).all()
    for id, in company:
        company_id.append(id)
    return company_id
    # property =  Property.query.with_entities(Property.name).all()
    # property_list = [value for value, in property]
    # com_dict = {}
    # data = {}
    # final_Data = []
    # for com in company:
    #     companyHasproperty = CompanyHasProperty.query.with_entities(
    #         CompanyHasProperty.p_id).filter(
    #             CompanyHasProperty.c_id == com.id).all()
    #     companyHasproperty_pid = [value for value, in companyHasproperty]
    #     company_pid_list = companyHasproperty_pid
    #     company_pname_list = []
    #     for id in company_pid_list:
    #         property = Property.query.filter(Property.id == id).first()
    #         company_pname_list.append(property.name)
    #     com_dict[com.name] = company_pname_list
    #     data = {}
    #     data['company_id'] = com.id
    #     data['company_name'] = com.name
    #     data['company_category'] = [com.category]
    #     data['company_link'] = com.link
    #     data['company_cause'] = company_pname_list
    #     final_Data.append(data)
    # return final_Data


def search_by_company_category(search=None):
    if search is None:
        return "Not Found"
    company_id = []
    company = Company.query.with_entities(
            Company.id).filter(Company.category.in_(search)).all()
    for id, in company:
        company_id.append(id)
    return company_id
    # property =  Property.query.with_entities(Property.name).all()
    # property_list = [value for value, in property]
    # com_dict = {}
    # final_Data = []
    # for com in company:
    #     companyHasproperty = CompanyHasProperty.query.with_entities(
    #         CompanyHasProperty.p_id).filter(
    #             CompanyHasProperty.c_id == com.id).all()
    #     companyHasproperty_pid = [value for value, in companyHasproperty]
    #     company_pid_list = companyHasproperty_pid
    #     company_pname_list = []
    #     for id in company_pid_list:
    #         property = Property.query.filter(Property.id == id).first()
    #         company_pname_list.append(property.name)
    #     com_dict[com.name] = company_pname_list
    #     data = {}
    #     data['company_id'] = com.id
    #     data['company_name'] = com.name
    #     data['company_category'] = [com.category]
    #     data['company_link'] = com.link
    #     data['company_cause'] = company_pname_list
    #     final_Data.append(data)
    # return final_Data


def search_by_company_cause(search=None):
    if search is None:
        return "Not Found"
    property = Property.query.with_entities(Property.id).filter(Property.name.in_(search)).all()
    property_id = []
    for id, in property:
        property_id.append(id)
    company_has_property = CompanyHasProperty.query.with_entities(CompanyHasProperty.c_id).filter(
        CompanyHasProperty.p_id.in_(property_id)).all()
    company_has_property_list = []
    for id, in company_has_property:
        company_has_property_list.append(id)
    company = Company.query.with_entities(Company.id).filter(Company.id.in_(company_has_property_list)).all()
    company_id = []
    for id, in company:
        company_id.append(id)
    return company_id


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def prepare_response(company_id=None):
    if company_id is None:
        return "Not Found"
    com_dict = {}
    final_Data = []
    company = Company.query.filter(Company.id.in_(company_id))
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
        if com.logo:
            data['company_logo'] = base64.b64encode(com.logo).decode('ascii')
        else:
            data['company_logo'] = ""
        final_Data.append(data)
    return final_Data

def search_company_based_on_filters(search_company_name=None,
                                    search_company_category=None,
                                    search_company_causes=None):
    company_causes = []
    company_category = []
    company = []
    if search_company_name != "":
        print(search_company_name)
        company = search_by_company_name(search_company_name)
        company_id = company
        print(company)
    if len(search_company_category) != 0:
        company_category = search_by_company_category(search_company_category)
        if  len(company) != 0:
            company_category = intersection(company, company_category)
        company_id = company_category
        print("SEARCH BY COMPANY CATEGORY = ", company_id)
    if len(search_company_causes) != 0:
        company_causes = search_by_company_cause(search_company_causes)
        if len(company) != 0:
            company_causes = intersection(company, company_causes)
        company_id = company_causes
        print("SEARCH BY COMPANY causes = ", company_id)

    if len(search_company_category) != 0 and len(search_company_causes) != 0:
        company_id = intersection(company_causes,company_category)
        print("COMPANY_IDS  = %s" , str(company_id))

    return prepare_response(company_id)