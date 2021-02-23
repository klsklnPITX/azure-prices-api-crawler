import requests
import json
import csv


BASE_URL = "https://prices.azure.com/api/retail/prices?$filter=location eq"

FIELDS = [
    "currencyCode",
    "retailPrice",
    "unitPrice",
    "location",
    "meterId",
    "meterName",
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


def csv_writer(data, filename):
    with open(f'{filename}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV headers
        writer.writerow(FIELDS)

        for value in data["Items"]:
            writer.writerow([
                value[FIELDS[0]],
                value[FIELDS[1]],
                value[FIELDS[2]],
                value[FIELDS[3]],
                value[FIELDS[4]],
                value[FIELDS[5]],
                value[FIELDS[6]],
                value[FIELDS[7]],
                value[FIELDS[8]],
                value[FIELDS[9]],
                value[FIELDS[10]],
                value[FIELDS[1]],
                value[FIELDS[12]],
                value[FIELDS[13]],
            ])


def get_next_page(json_data):
    if json_data["NextPageLink"]:
        return json_data["NextPageLink"]
    return False


def call_next_page(current_page_data):
    if not get_next_page(current_page_data):
        return False

    next_page_url = get_next_page(current_page_data)
    r = requests.get(next_page_url)
    new_data = json.loads(json.dumps(r.json()))
    return new_data


def get_api_data(location):
    r = requests.get(BASE_URL+f" '{location}'")
    data = json.loads(json.dumps(r.json()))
    print("page 1")
    if get_next_page(data):
        next_page_exists = True
        new_data = call_next_page(data)
        data.update(new_data)
        print("page 2")

    while next_page_exists:
        new_data = call_next_page(new_data)
        if new_data:
            data.update(new_data)
            print(get_next_page(new_data))
        else:
            next_page_exists = False
            print("done")

    return data


data = get_api_data("EU West")
csv_writer(data, "eu-west-prices")
