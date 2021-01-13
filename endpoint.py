#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort
import logging
import odoolib

app = Flask(__name__)


@app.route('/Login', methods=['GET'])
def login():
    """
    input: http://localhost:8000/Login?Username=test&Password=123456&Company=wso
    @return: result
    """
    result = {}
    if request.method == 'GET':
        user_name = request.args.get('Username', False)
        password = request.args.get('Password', False)
        company = request.args.get('Company', False)
        if user_name and password and company:
            if company == 'Tinnakorn-TKM':
                connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                    login=user_name, password=password)
                connection.check_login()
                result = {
                    "userId": connection.user_id
                }
            elif company == 'Tinnakorn-TKC':
                connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                    login=user_name, password=password)
                connection.check_login()
                result = {
                    "userId": connection.user_id
                }
            elif company == 'wso':
                connection = odoolib.get_connection(hostname="192.168.1.25", database="wso", \
                                                    login=user_name, password=password)
                connection.check_login()
                # user_model = connection.get_model("res.users")
                # ids = user_model.search([("login", "=", user_name), ('password', '=', password)])
                # user_info = user_model.read(ids[0], ["name"])
                result = {
                    "userId": connection.user_id
                }
    # elif request.method == 'POST':
    #     print(request.json())
    return jsonify(result), 200


@app.route('/getCompanies', methods=['GET'])
def get_companies():
    """
    input : http://localhost:8000/getCompanies
    @return: result
    """
    result = []
    if request.method == 'GET':
        result = [
            {
                "key": "Tinnakorn-TKM",
                "value": "Tinnakorn Marketing CO., Ltd."
            },
            {
                "key": "Tinnakorn-TKC",
                "value": "Tinnakorn Chemical and Supply Co., Ltd."
            },
            {
                "key": "wso",
                "value": "KERDOS Co., Ltd."
            }
        ]
    return jsonify(result), 200


@app.route('/getContactType', methods=['GET'])
def get_contact_type():
    result = []
    if request.method == 'GET':
        result = [
            {
                "key": "contact",
                "value": "Contact"
            },
            {
                "key": "default",
                "value": "Default"
            },
            {
                "key": "invoice",
                "value": "Invoice"
            },
            {
                "key": "delivery",
                "value": "Shipping"
            },
            {
                "key": "other",
                "value": "Other"
            }
        ]
    return jsonify(result), 200


@app.route('/getProducts', methods=['GET'])
def get_products():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    product_id = request.args.get('productId', 0)
    product_name = request.args.get('productName', False)

    result = []

    if user_name and password and company and (product_id or product_name):
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            product_model = connection.get_model("product.product")
            product_ids = product_model.search(['|', ("id", "=", product_id), ('name', 'ilike', product_name)],
                                               order='name')
            record_count = 0
            do_count = 0
            for product_id in product_ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        product_info = product_model.read(product_id,
                                                          ["id", "company_id", "categ_id", "name", "qty_available",
                                                           "incoming_qty", "virtual_available", "sale_delay",
                                                           "manu_short", "origin_country", "product_function",
                                                           "fin_categ_id", "product_tmpl_id", "finishedCategoryList"])
                        result.append(product_info)
                record_count += 1
    # sample_result = [
    #     {
    #         "id": 77,
    #         "company_id": [
    #             1,
    #             "KERDOS Co., Ltd."
    #         ],
    #         "categ_id": [
    #             1,
    #             "All"
    #         ],
    #         "name": "WSO-D201SWL  Die Casting Lubricant (WSO) (1000 kg/ibc tank)",
    #         "qty_available": 1000.0,
    #         "incoming_qty": 0.0,
    #         "virtual_available": 1000.0,
    #         "sale_delay": 7.0,
    #         "manu_short": "WSO",
    #         "origin_country": "-",
    #         "product_function": False,
    #         "fin_categ_id": [],
    #         "product_tmpl_id": [
    #             123,
    #             "WSO-D201SWL  Die Casting Lubricant (WSO) (1000 kg/ibc tank)"
    #         ],
    #         "finishedCategoryList": []
    #     }
    # ]
    return jsonify(result), 200


@app.route('/getCategories', methods=['GET'])
def get_categories():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    result = []
    if user_name and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            category_model = connection.get_model("crm.case.categ")
            category_ids = category_model.search([('object_id.model', '=', 'crm.phonecall')],
                                                 order='name')
            for categ_id in category_ids:
                categ_info = category_model.read(categ_id,
                                                 ["id", "name"])
                result.append(categ_info)
    return jsonify(result), 200


@app.route('/getCountries', methods=['GET'])
def get_countries():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    result = []
    result.append({
        "id": 0,
        "name": "--Select--"
    })
    if user_name and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            model = connection.get_model("res.country")
            ids = model.search([], order='name')
            for id in ids:
                info = model.read(id, ["id", "name"])
                result.append(info)
    return jsonify(result), 200


@app.route('/getCustomers', methods=['GET'])
def get_customers():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    customer_id = request.args.get('customerId', 0)
    customer_name = request.args.get('customerName', False)

    result = []
    if user_name and password and company and (customer_id or customer_name):
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            model = connection.get_model("res.partner")
            ids = model.search(['|', ("id", "=", customer_id), ('name', 'ilike', customer_name)],
                               order='name')
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        info = model.read(id,
                                          ["id", "company_id", "name", "street", "street2",
                                           "city", "zip", "function",
                                           "phone", "mobile", "email_print",
                                           "fax", "comment", "country_id", "is_company", "child_ids"])
                        fullAddress = "{} {} {} {}".format(info['street'], info['street2'], info['city'], info['zip'])
                        info['fullAddress'] = fullAddress
                        info['contactList'] = info['chil_ids']
                        info.pop('chil_ids', None)
                        result.append(info)
                record_count += 1

    return jsonify(result), 200


@app.route('/getDashboardDetails', methods=['GET'])
def get_dashboard_details():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    result = {
        "leadingIndicator": {
            "customerVisitThisWeek": 0,
            "newCustomerAcquiredThisMonth": 0,
            "newCustomerAcquiredThisYear": 0,
            "newOpportunitiesThisMonth": 0,
            "newOpportunitiesThisYear": 0,
            "ongoingOpportunities": 0
        },
        "laggingIndicator": {
            "thisMonth": {
                "repeateSellingActual": 0,
                "repeateSellingTarget": 0,
                "crossSellingActual": 0,
                "crossSellingTarget": 0,
                "newCustomerActual": 0,
                "newCustomerTarget": 0,
                "biddingActual": 0,
                "biddingTarget": 0
            },
            "thisYear": {
                "repeateSellingActual": 0,
                "repeateSellingTarget": 0,
                "crossSellingActual": 0,
                "crossSellingTarget": 0,
                "newCustomerActual": 0,
                "newCustomerTarget": 0,
                "biddingActual": 0,
                "biddingTarget": 0
            }
        }
    }
    return jsonify(result), 200


@app.route('/getHomeScreenData', methods=['GET'])
def get_home_screen_data():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    result = {
        "customerVisitThisWeek": 0,
        "ongoingOpportunities": 0,
        "repeateSellingActual": 0,
        "repeateSellingTarget": 0,
        "crossSellingActual": 0,
        "crossSellingTarget": 0,
        "newCustomerActual": 0,
        "newCustomerTarget": 0
    }
    return jsonify(result), 200


@app.route('/getLoggedCalls', methods=['GET'])
def get_logcalls():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    log_call_name = request.args.get('loggedCallName', 0)
    customer_id = request.args.get('CustomerId', False)

    result = []

    if user_name and password and company and (customer_id or log_call_name):
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            model = connection.get_model("crm.phonecall")
            ids = model.search(['|', ("partner_id", "=", int(customer_id)), ('name', 'ilike', u'ตามงาน')],
                               order='date')
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        product_info = model.read(id,
                                                  ["id", "date", "categ_id", "partner_id", "name",
                                                   "description"])
                        result.append(product_info)
                record_count += 1
    # sample_result = [
    #     {
    #         "id": 77,
    #         "company_id": [
    #             1,
    #             "KERDOS Co., Ltd."
    #         ],
    #         "categ_id": [
    #             1,
    #             "All"
    #         ],
    #         "name": "WSO-D201SWL  Die Casting Lubricant (WSO) (1000 kg/ibc tank)",
    #         "qty_available": 1000.0,
    #         "incoming_qty": 0.0,
    #         "virtual_available": 1000.0,
    #         "sale_delay": 7.0,
    #         "manu_short": "WSO",
    #         "origin_country": "-",
    #         "product_function": False,
    #         "fin_categ_id": [],
    #         "product_tmpl_id": [
    #             123,
    #             "WSO-D201SWL  Die Casting Lubricant (WSO) (1000 kg/ibc tank)"
    #         ],
    #         "finishedCategoryList": []
    #     }
    # ]
    return jsonify(result), 200


@app.route('/getOpportunities', methods=['GET'])
def get_opportunities():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    opportunity_name = request.args.get('opportunityName', 0)
    filter = request.args.get('filter', False)
    customer_id = request.args.get('CustomerId', False)

    result = []

    if user_name and password and company and (customer_id or opportunity_name):
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=user_name, password=password)
            connection.check_login()
        if connection:
            model = connection.get_model("crm.lead")
            ids = model.search([("partner_id", "=", int(customer_id)),
                                ('user_id', '=', connection.user_id)],
                               order='name')
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        product_info = model.read(id,
                                                  ["id", "name", "partner_name", "contact_name", "partner_id",
                                                   "source_id", "country_id", "stage_id", "street", "street2",
                                                   "city", "zip", "user_email", "function", "phone", "mobile", "fax",
                                                   "priority", "description", "planned_revenue", "probability",
                                                   "color"])
                        result.append(product_info)
                record_count += 1
    sample_result = [
        {
            "id": "1889",
            "name": "C283XS for ball mill at SCG Thaluang",
            "partner_name": "บริษัท ปูนซิเมนต์ไทย (ท่าหลวง) จำกัด",
            "contact_name": False,
            "partner_id": [
                8294,
                "บริษัท ปูนซิเมนต์ไทย (ท่าหลวง) จำกัด (สาขาที่ 00003), Autthapol Bainium"
            ],
            "source_id": False,
            "country_id": False,
            "stage_id": [
                20,
                "Lab Industry"
            ],
            "street": False,
            "street2": False,
            "city": False,
            "zip": False,
            "user_email": "autthapol@tinnakorn.com",
            "function": False,
            "phone": "036-218-400",
            "mobile": False,
            "fax": False,
            "priority": "2",
            "description": False,
            "planned_revenue": 0.0,
            "probability": 90.0,
            "color": "Defualt"
        }
    ]
    return jsonify(result), 200


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
