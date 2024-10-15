import requests
import json

key = ''
with open('instance/api.json', 'r') as file:
    data = json.load(file)
    key = data['VehicleEnquiryAPI']

def search_reg(reg):
    api_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    json = {"registrationNumber": reg}
    headers = {"Content-Type":"application/json","Accept":"application/json", "x-api-key": key}
    response = requests.post(api_url, json=json, headers=headers)

    data = response.json()

    return data