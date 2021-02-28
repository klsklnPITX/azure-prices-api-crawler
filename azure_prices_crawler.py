import requests
import json
import csv


BASE_URL = "https://prices.azure.com/api/retail/prices?$filter=location eq"
LOCATIONS = ["DE West Central", "EU West"]
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


def get_api_data(*locations, separated_files=True, filename="output"):
    for idx, location in enumerate(locations):
        if separated_files:
            write_type = "w"
            filename = location
        if idx == 0 and not separated_files:
            write_type = "w"
        elif idx > 0 and not separated_files:
            write_type = "a"

        r = requests.get(BASE_URL+f" '{location}'")
        data = json.loads(json.dumps(r.json()))
        csv_writer(data, filename, write_type)

        if get_next_page(data):
            next_page_exists = True
            new_data = data
        while next_page_exists:
            new_data = call_next_page(new_data)
            if new_data:
                print(get_next_page(new_data))
                csv_writer(new_data, filename, "a")
            else:
                next_page_exists = False
                print(f"Done with: {location}")


get_api_data(*LOCATIONS, separated_files=False)
