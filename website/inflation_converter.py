import datetime
import csv
from .currency_converter import update_ecb_file

def prepare_converter():
    rates = {}
    filename = 'instance/inflation_data.csv'
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, ('year', 'rate'))
        for line in reader:
            rates[line['year']] = line['rate']
    return rates

def inflation_convert(data):
    rates = prepare_converter()
    data_inflated = []
    for line in data:
        year = line['x'].split('-')[0]
        cost = float(line['y'])
        cost_converted = round(cost * float(rates[year]), 4)
        data_inflated.append({'x': line['x'], 'y': cost_converted, 'currency': line['currency']})
    return data_inflated