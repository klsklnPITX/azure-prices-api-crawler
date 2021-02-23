import requests
import json


BASE_URL = "https://prices.azure.com/api/retail/prices?$filter=location eq"

FIELDS = [
    "currencyCode",
    "retailPrice",
    "unitPrice",
    "location",
    "meterId",
    "meterName,"
    "productId",
    "productName",
    "skuName",
    "armSkuName",
    "serviceName",
    "serviceFamily",
    "unitOfMeasure",
    "type"
]

""" 
ToDo:
* Call API with location param
* Get values for required fields
* Save to CSV and excel file
"""


def call_api(location):
    r = requests.get(BASE_URL+f" '{location}'")
    data = json.loads(json.dumps(r.json()))

    # Get next page
    if data["NextPageLink"]:
        print(data["NextPageLink"])
    # print(data)


call_api("EU West")
