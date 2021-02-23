import requests
import json
import csv


BASE_URL = "https://prices.azure.com/api/retail/prices?$filter=location eq"
# LOCATION = "EU West"
LOCATION = "DE West Central"


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


def test_for_machine(machine, data):
    for value in data["Items"]:
        if machine in value["meterName"]:
            print(f"Found: {value['meterName']}")


def csv_writer(data, filename, write_type):
    with open(f'{filename}.csv', write_type, newline="") as file:
        writer = csv.writer(file)

        if write_type == "w":
            writer.writerow(FIELDS)

        for value in data["Items"]:
            writer.writerow([value[x] for x in FIELDS])


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
    csv_writer(data, LOCATION, "w")
    test_for_machine("NV16as", data)

    if get_next_page(data):
        next_page_exists = True
        new_data = data
    while next_page_exists:
        new_data = call_next_page(new_data)
        if new_data:
            test_for_machine("NV16as", new_data)
            print(get_next_page(new_data))
            csv_writer(new_data, LOCATION, "a")
        else:
            next_page_exists = False
            print("done")


get_api_data(LOCATION)
