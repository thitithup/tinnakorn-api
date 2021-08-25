#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort
import logging
import odoolib
import json

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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getProducts', methods=['GET'])
def get_products():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    product_id = request.args.get('productId') or 0
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

            product_ids = False
            if product_name != "":
                product_ids = product_model.search([('name', 'ilike', product_name)],
                                                   order='name')
            if product_id > 0 and product_name == "":
                product_ids = product_model.search([("id", "=", product_id)],
                                                   order='name')
            if product_id > 0 and product_name != "":
                product_ids = product_model.search(['|', ("id", "=", product_id),('name', 'ilike', product_name)],
                                                   order='name')
            if product_ids:
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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
        # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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

                        fullAddress = info["street"]

                        if info["street2"]:
                            fullAddress = fullAddress + info["street2"]
                        elif info["city"]:
                            fullAddress = fullAddress + info["city"]
                        elif info["zip"]:
                            fullAddress = fullAddress + info["zip"]

                        info['fullAddress'] = fullAddress

                        info['contactList'] = info['child_ids']
                        info.pop('child_ids', None)

                        result.append(info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


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
    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getPriorities', methods=['GET'])
def get_priorities():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)

    result = [
        {
            "key": "0",
            "value": "Very Low"
        },
        {
            "key": "1",
            "value": "Low"
        },
        {
            "key": "2",
            "value": "Normal"

        },
        {
            "key": "3",
            "value": "High"
        },
        {
            "key": "4",
            "value": "Very High"
        }
    ]

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

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getOpportunitiesFilter', methods=['GET'])
def get_opportunitiesFilter():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)

    result = [
        {
            "key": "show all",
            "value": "Show ALL"
        },
        {
            "key": "new",
            "value": "New"
        },
        {
            "key": "on going",
            "value": "On Going"
        },
        {
            "key": "done",
            "value": "Done"
        }
    ]

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

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getReasons', methods=['GET'])
def get_Reasons():
    user_id = int(request.args.get('UserId', 0))
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10

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
            model = connection.get_model("ineco.ship.late.reason")
            ids = model.search([])
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        reason_info = model.read(id, ["id", "name"])
                        result.append(reason_info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getStages', methods=['GET'])
def get_stages():
    user_id = int(request.args.get('UserId', 0))
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10

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
            model = connection.get_model("crm.case.stage")
            ids = model.search([])
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        stages_info = model.read(id, ["id", "name"])
                        result.append(stages_info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getTaskMessage', methods=['GET'])
def get_taskmessage():
    user_id = int(request.args.get('UserId', 0))
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10

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
            model = connection.get_model("ineco.web.task")
            ids = model.search([])
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        taskmessage_info = model.read(id, ["id", "name", "notes", "state", "create_date"])
                        result.append(taskmessage_info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getWebTaskType', methods=['GET'])
def get_webtasktype():
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)

    result = [
        {
            "key": "New SO",
            "value": "New SO"
        },
        {
            "key": "New Quotation",
            "value": "New Quotation"
        },
        {
            "key": "Request Documents",
            "value": "Request Documents"
        },
        {
            "key": "Others",
            "value": "Others"
        }
    ]

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

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getSalesOrders', methods=['GET'])
def get_salesorders():
    user_id = int(request.args.get('UserId', 0))
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    customer_id = int(request.args.get('CustomerId', 0))
    flag = request.args.get('flgIsPending', False)

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
            model = connection.get_model("sale.order")
            model2 = connection.get_model("sale.order.line")
            model_tax = connection.get_model("account.tax")

            ids = model.search([("partner_id", "=", customer_id)])
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        saleorder_info = model.read(id,
                                                    ["id", "name", "partner_id", "partner_invoice_id", "currency_id",
                                                     "partner_shipping_id", "date_order", "requested_date",
                                                     "client_order_ref", "state", "order_line"])

                        line_ids = model2.search([("id", "in", saleorder_info["order_line"])])
                        for line_id in line_ids:
                            saleorderline_info = model2.read(line_id, ["id", "name", "product_id",
                                                                       "product_uom_qty", "product_uom", "price_unit",
                                                                       "price_subtotal", "tax_id", "order_id"])

                            saleorder_info['saleOrderLineList'] = [saleorderline_info]

                            tax_id = saleorderline_info["tax_id"]

                            tax_ids = model_tax.search([("id","in",tax_id)])
                            for id in tax_ids:
                                tax_info = model_tax.read(id,["id","name"])

                                saleorderline_info["taxList"] = [tax_info]

                            result.append(saleorder_info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/getSalesPriceRequest', methods=['GET'])
def get_salepricereq():
    user_id = int(request.args.get('UserId', 0))
    user_name = request.args.get('Username', False)
    password = request.args.get('Password', False)
    company = request.args.get('Company', False)
    offset = request.args.get('Offset', False) or 0
    page_size = request.args.get('pazeSize', False) or 10
    request_name = request.args.get('requestName', False)
    customer_id = request.args.get('customerId', 0)
    customer_name = request.args.get('customerName', False)

    result = []

    if user_name and password and company and customer_id:
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
            model = connection.get_model("sale.price.req")
            model2 = connection.get_model("sale.price.req.line")

            ids = model.search(['|', ("name", "=", request_name), ("partner_id", "=", customer_id)])
            record_count = 0
            do_count = 0
            for id in ids:
                if record_count >= int(offset):
                    do_count += 1
                    if do_count <= int(page_size):
                        salepricereq_info = model.read(id, ["id", "name", "partner_id", "partner_fin_product",
                                                            "approver_id", "request_date",
                                                            "state", "line_ids"])

                        # print(salepricereq_info)
                        line_ids = model2.search([("id", "in", salepricereq_info["line_ids"])])
                        for line_id in line_ids:
                            salepricereqline_info = model2.read(line_id,
                                                                ["product_id", "is_new_product",
                                                                 "quantity_time", "quantity_year",
                                                                 "uom", "product_name",
                                                                 "product_comment", "product_comp_country",
                                                                 "product_comp_price", "product_comp_unit",
                                                                 "product_app_price", "product_app_unit",
                                                                 "product_app_comment"])
                            salepricereq_info['saleRequestLines'] = salepricereqline_info

                            result.append(salepricereq_info)
                record_count += 1

    # return jsonify(result), 200
    return json.dumps(result, ensure_ascii=False, encoding='utf8')


@app.route('/postCustomers', methods=['POST'])
def post_customers():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    customer_id = input["CustomerId"]
    customer_name = input["CustomerName"]
    street = input["Address1"]
    street2 = input["Address2"]
    city = input["City"]
    zip = input["Zip"]
    customer_type = input["Customertype"]
    phone = input["Phone"]
    mobile = input["Mobile"]
    email_print = input["EmailPrint"]

    new_customer = {
        'name': customer_name,
        'street': street,
        'street2': street2,
        'city': city,
        'zip': zip,
        'phone': phone,
        'mobile': mobile,
        'user_id': user_id,
        'is_company': True,
        # 'email_print':email_print
    }

    result = {}

    if username and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=username, password=password)
            connection.check_login()

        if connection:
            partner_model = connection.get_model("res.partner")

            ids = partner_model.search([("name", "=", customer_name), ("phone", "=", phone), ("mobile", "=", mobile)])

            if not ids:
                create_user = partner_model.create(new_customer)
                result["customerId"] = create_user

            else:
                result["customerId"] = ids[0]

    return jsonify(result), 200


@app.route('/postCustomerContact', methods=['POST'])
def post_customercontact():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    customer_id = input["CustomerId"]
    customer_contact_id = input["CustomerContactId"]
    contact_name = input["ContactName"]
    contact_type = input["Contacttype"]
    phone = input["Phone"]
    mobile = input["Mobile"]
    email_print = input["EmailPrint"]
    jobposition = input["JobPosition"]

    new_customer = {
        'name': contact_name,
        # 'contact_type':contact_type,
        'parent_id': customer_id,
        'phone': phone,
        'mobile': mobile,
        'user_id': user_id,
        'function': jobposition,
        # 'email_print':email_print
    }

    result = {}

    if username and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=username, password=password)
            connection.check_login()

        if connection:
            partner_model = connection.get_model("res.partner")

            ids = partner_model.search([("name", "=", contact_name), ("phone", "=", phone), ("mobile", "=", mobile)])

            if not ids:
                create_contact = partner_model.create(new_customer)
                result["customerContactId"] = create_contact

            else:
                result["customerContactId"] = ids[0]

    return jsonify(result), 200


@app.route('/postLoggedCalls', methods=['POST'])
def post_loggedcalls():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    log_id = input["LoggedCallId"]
    customer_id = input["CustomerId"]
    opportunity_id = input["OpportunityId"]
    date = input["Date"]
    log_name = input["LoggedName"]
    description = input["Description"]
    category_id = input["CategoryId"]

    new_log = {
        'partner_id': customer_id,
        'opportunity_id': opportunity_id,
        'date': date,
        'name': log_name,
        'description': description,
        'categ_id': category_id,
        'user_id': user_id
    }

    result = {}

    if username and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=username, password=password)
            connection.check_login()

        if connection:
            crm_logcall_model = connection.get_model("crm.phonecall")

            ids = crm_logcall_model.search([("name", "=", log_name), ("user_id", "=", user_id), ("date", "=", date)])

            if not ids:
                create_log = crm_logcall_model.create(new_log)
                result["loggedCallId"] = create_log

            else:
                result["loggedCallId"] = ids[0]

    return jsonify(result), 200


@app.route('/postOpportunities', methods=['POST'])
def post_opportunities():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    opportunities_id = input["OpportunitiesId"]
    customer_id = input["CustomerId"]
    opportunities_name = input["OpportunitiesName"]
    contact_name = input["ContactName"]
    stage_id = input["StageId"]
    description = input["Description"]
    priority = input["Priority"]
    plannedrevenue = input["PlannedRevenue"]
    probability = input["Probability"]
    type = input["type"]

    new_opp = {
        'name': opportunities_name,
        'partner_id': customer_id,
        'contact_name': contact_name,
        'stage_id': stage_id,
        'description': description,
        'priority': priority,
        'plannedrevenue': plannedrevenue,
        'probability': probability,
        'type': type,
        'user_id': user_id
    }

    result = {}

    if username and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=username, password=password)
            connection.check_login()

        if connection:
            crm_lead_model = connection.get_model("crm.lead")

            ids = crm_lead_model.search([])

            if not ids:
                create_opp = crm_lead_model.create(new_opp)
                result["opportunitiesId"] = create_opp

            else:
                result["opportunitiesId"] = ids[0]

    return jsonify(result), 200


@app.route('/postTaskMessage', methods=['POST'])
def post_taskmessage():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    message_type = input["MessageType"]
    message = input["Message"]
    attachment = input["Attachment"]


    new_message = {
        'name': message,
        'message_type': message_type,
        'attachment': attachment,
        'user_id': user_id
    }

    result = {}

    if username and password and company:
        connection = False
        if company == 'Tinnakorn-TKM':
            connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'Tinnakorn-TKC':
            connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                login=username, password=password)
            connection.check_login()
        elif company == 'wso':
            connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                login=username, password=password)
            connection.check_login()

        if connection:
            web_task_model = connection.get_model("ineco.web.task")

            ids = web_task_model.search([])

            if not ids:
                create_message = web_task_model.create(new_message)
                result["webTaskId"] = create_message

            else:
                result["webTaskId"] = ids[0]

    return jsonify(result), 200


@app.route('/postSalesPriceRequest', methods=['POST'])
def post_salespricerequest():
    input = json.loads(request.data)

    user_id = input["UserId"]
    username = input["username"]
    password = input["Password"]
    company = input["Company"]
    header_id = input["HeaderId"]
    customer_product = input["CustomerProduct"]
    customer_id = input["CustomerId"]
    approver_id = input["ApproverId"]
    request_date = input["RequestDate"]
    SalePriceRequestLines = input["SalePriceRequestLines"]

    for sale_req_id in SalePriceRequestLines:
        prodcut_id = sale_req_id["ProductId"]
        new_product = sale_req_id["IsNewProduct"]
        qty_perorder = sale_req_id["QuantityPerOrder"]
        qty_peryear = sale_req_id["QuantityPerYear"]
        unitofmeasure = sale_req_id["UnitOfMeasure"]

        new_req = {
            'partner_fin_product':customer_product,
            'partner_id':customer_id,
            'approver_id':approver_id,
            'request_date':request_date,
            'user_id':user_id
            # 'header_id':header_id
        }

        new_req_line = {
            'product_id': prodcut_id,
            'is_new_product':new_product,
            'quantity_time':qty_perorder,
            'quantity_year':qty_peryear,
            'uom':unitofmeasure

        }

        result = {}

        if username and password and company:
            connection = False
            if company == 'Tinnakorn-TKM':
                connection = odoolib.get_connection(hostname="192.168.1.23", database=company, \
                                                    login=username, password=password)
                connection.check_login()
            elif company == 'Tinnakorn-TKC':
                connection = odoolib.get_connection(hostname="192.168.1.21", database=company, \
                                                    login=username, password=password)
                connection.check_login()
            elif company == 'wso':
                connection = odoolib.get_connection(hostname="192.168.1.25", database=company, \
                                                    login=username, password=password)
                connection.check_login()

            if connection:
                sale_req_model = connection.get_model("sale.price.req")
                sale_req_line_model = connection.get_model("sale.price.req.line")

                ids = sale_req_model.search([("partner_id","=",customer_id),("partner_fin_product","=",customer_product),
                                             ("approver_id","=",approver_id),("request_date","=",request_date)])

                if not ids:
                    create_sale_req = sale_req_model.create(new_req)
                    result["salesPriceRequestId"] = create_sale_req
                    new_req_line["request_id"] = create_sale_req
                    create_sale_req_line = sale_req_line_model.create(new_req_line)

                else:
                    result["salesPriceRequestId"] = ids[0]
                    new_req_line["request_id"] = ids[0]
                    create_sale_req_line = sale_req_line_model.create(new_req_line)

        return jsonify(result), 200


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
