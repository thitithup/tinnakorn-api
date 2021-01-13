# tinnakorn-api

Login - module:
http://192.168.1.12:8000/Login?Username=test&Password=1234&Company=wso
http://192.168.1.12:8000/getCompanies?Username=test&Password=1234&Company=wso

User - module:
http://192.168.1.12:8000/getUsers?Username=test&Password=1234&Company=wso&Offset=0&pazeSize=10&customerId=25&customerName=test

Product - module:
http://192.168.1.12:8000/getProducts?UserId=74&Username=test&Password=1234&Company=wso&Offset=0&pazeSize=10&productId=77&productName=test

Categories - module:
http://192.168.1.12:8000/getCategories?UserId=74&Username=test&Password=1234&Company=wso

Countries - module:
http://192.168.1.12:8000/getCountries?UserId=74&Username=test&Password=1234&Company=wso

Customer - module:
http://192.168.1.12:8000/getCustomers?UserId=74&Username=test&Password=1234&Company=wso&Offset=0&pazeSize=10&customerId=1881&customerName=test
http://192.168.1.12:8000/postCustomers
http://192.168.1.12:8000/postCustomerContact
http://192.168.1.12:8000/getContactType

Dashboard - module:
http://192.168.1.12:8000/getDashboardDetails?UserId=74&Username=test&Password=1234&Company=wso

HomeScreen - module:
http://192.168.1.12:8000/getHomeScreenData?UserId=74&Username=test&Password=1234&Company=wso

LoggedCalls - module:
http://192.168.1.12:8000/getLoggedCalls?UserId=74&Username=test&Password=1234&Company=wso&offset=0&pazeSize=10&&loggedCallName=Follow&CustomerId=1378
http://192.168.1.12:8000/postLoggedCalls

Opportunities - module:
http://192.168.1.12:8000/getOpportunities?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM&offset=0&pazeSize=10&&opportunityName=test&CustomerId=2175&filter=test
http://192.168.1.12:8000/getPriorities?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM
http://192.168.1.12:8000/getOpportunitiesFilter?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM
http://192.168.1.12:8000/postOpportunities

Reasons - module:
http://192.168.1.12:8000/getReasons?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM

Stages - module:
http://192.168.1.12:8000/getStages?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM

TaskMessage - module:
http://192.168.1.12:8000/getTaskMessage?UserId=79&Username=test&Password=1234&Company=Tinnakorn-TKM&Offset=0&pazeSize=10
http://192.168.1.12:8000/getWebTaskType
http://192.168.1.12:8000/postTaskMessage


SaleOrder - module:
http://192.168.1.12:8000/getSalesOrders?UserId=74&Username=test&Password=1234&Company=wso&CustomerId=1772&flgIsPending=true
http://192.168.1.12:8000/postUrgentReport


SalesPriceRequest - module:
http://192.168.1.12:8000/getSalesPriceRequest?UserId=267&Username=test&Password=1234&Company=Tinnakorn-TKC&offset=0&pazeSize=10&requestName=SPR171003&customerId=6523
http://192.168.1.12:8000/postSalesPriceRequest