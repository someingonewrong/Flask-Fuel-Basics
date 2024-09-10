from flask import request
from .models import Record
from . import db
from .currency_converter import update_ecb_file
import datetime

from os import path

def get_vehicles(current_user):
    try:
        vehicles_query = Record.query.filter_by(user_id = current_user.id)
        vehicles = set()

        for vehicle in vehicles_query:
            vehicles.add(vehicle.vehicle)

        return vehicles
    except Exception as e:
        print('Something is broken. The error: \n' + str(e))
        return []

def post_record(current_user, vehicles = []):
    date_test = request.form.get('date').split('-')
    try: date_convert = datetime.date(int(date_test[0]), int(date_test[1]), int(date_test[2]))
    except: date_convert = datetime.date.today()

    record = Record(vehicle = request.form.get('vehicle'),
                    date = date_convert,
                    mileage = request.form.get('mileage'),
                    litres = request.form.get('litres'),
                    cost = request.form.get('cost'),
                    currency = request.form.get('currency'),
                    user_id = current_user.id)

    error_message = ''
        
    if len(record.vehicle) < 1:
        error_message += 'Invalid Vehicle    ' 
        
    if len(record.mileage) < 1:
        error_message += 'Invalid Mileage    '
        
    if len(record.litres) < 1:
        error_message += 'Invalid Litres    '
        
    if len(record.cost) < 1:
        error_message += 'Invalid Cost    '
    
    if len(error_message) > 0:
        return error_message
    else:
        return check_input(record, vehicles, current_user)

def check_input(record, vehicles, current_user):
    url = str(request.base_url.split('/')[-1])
    error_message = ''
    mileages = Record.query.filter_by(user_id = current_user.id, vehicle = record.vehicle)
    mileages_useable = []

    for mileage in mileages:
        mileages_useable.append(mileage.mileage)

    try: mileage_last = sorted(mileages_useable)[-1]
    except: mileage_last = 0

    if url == 'add-record':
        if record.vehicle not in vehicles: 
            error_message += 'Somehow you\'ve inputted an invalid vehicle    '

        if mileage_last > int(record.mileage):
            error_message += 'Mileage can not be smaller than the last mileage: ' + str(mileage_last) + '    '
    
    try: record.litres = int_convert(record.litres)
    except: error_message += 'Litres could not be convertered to required format    '
    
    try: record.cost = int_convert(record.cost)
    except: error_message += 'Cost could not be convertered to required format    '

    if len(error_message) > 0:
        return error_message
    else:
        db.session.add(record)
        db.session.commit()
        success_list = 'Data Added:    Date: ' + str(record.date) + '   Vehicle: ' + str(record.vehicle) + '   Mileage: ' + str(record.mileage) + '   Litres: ' + str(record.litres) + '   Cost: ' + str(record.cost) + '   Currency: ' + str(record.currency)
        return success_list

def int_convert(input):
    input_split = input.split('.')
    if len(input_split) > 2 or int(input_split[0]) < 0:
        raise
    try:
        output = int(input_split[0]) * 100
        if len(input_split[1]) == 1:
            output += int(input_split[1]) * 10
        elif int(input_split[1]) < 0: raise
        else:
            output += int(input_split[1])
    except:
        try: output = int(input) * 100
        except: raise
    return output

def fetch_records(current_user, vehicle = '*', column = 'id', updown = 'DESC'):
    temp = f'Record.{column}'

    if vehicle == '*' and column == 'id':
        records = Record.query.filter_by(user_id = current_user.id).all()
    elif vehicle != '*' and column == 'id':
        records = Record.query.filter_by(user_id = current_user.id, vehicle = vehicle).all()
    elif vehicle == '*' and column != 'id':
        records = Record.query.filter_by(user_id = current_user.id).order_by(Record.__dict__[column]).all()
    else:
        records = Record.query.filter_by(user_id = current_user.id, vehicle = vehicle).order_by(Record.__dict__[column]).all()
    table = []
    for record in records:
        table.append([record.id, record.vehicle, record.date, record.mileage, record.litres, record.cost, record.currency, record.user_id, record.date_uploaded])

    if updown != 'ASC':
        table.reverse()

    return table

def delete_record(current_user, records):
    line_n = 0
    try:
        for line in records:
            if line.isnumeric():
                line_n += 1
                Record.query.filter(Record.user_id == current_user.id, Record.id == line).delete()
        db.session.commit()
        return ['Deleted ' + str(line_n) + ' records', 'message']
    except:
        return ['An error occured', 'error']
    
def find_record(current_user, id):
    return Record.query.filter(Record.user_id == current_user.id, Record.id == id).all()[0]
    
def get_date_mileage(current_user, vehicle, scale):
    all_data = Record.query.filter(Record.user_id == current_user.id, Record.vehicle == vehicle).order_by(Record.mileage).all()
    labels = []
    data = []
    date = 0
    min = 0
    max = 0

    for line in all_data:
        date = datetime.datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        data.append({"x": date_output, "y": int(line.mileage)})

        if scale == 'instance':
            labels.append(date_output)

        if min == 0:
            min = date

    max = date

    if scale == 'date':
        while min != max:
            labels.append(min.strftime('%Y-%m-%d'))
            temp = min + datetime.timedelta(days=1)
            min = temp
        labels.append(date_output)

    return [labels, data]

def get_fuel_cost(current_user, vehicle, scale, currency_con):
    all_data = Record.query.filter(Record.user_id == current_user.id, Record.vehicle == vehicle).order_by(Record.mileage).all()
    labels = []
    data = []
    temp = 1.5
    date = 0
    min = 0
    max = 0

    if currency_con == 'Y':
        c = update_ecb_file()
        print(c)

    for line in all_data:
        date_0 = datetime.datetime.strptime(str(line.date), '%Y-%m-%d')
        date_1 = date_0 + datetime.timedelta(days=1)
        date_output = str(line.date)
        try: 
            if int(line.cost)/(int(line.litres)) != 0:
                try:
                    if currency_con == 'Y':
                        line.cost = c.convert(int(line.cost), line.currency, 'GBP', date=line.date)
                except Exception as e: print(e)
                temp = "%.2f" % (int(line.cost)/int(line.litres))
        except: pass

        if scale == 'instance':
            labels.append(date_output)

        try:
            if labels[-1] == labels[-2]:
                date_output = str(date_1.strftime('%Y-%m-%d'))
                if date_output == labels[-2]:
                    date_output = str(date_1.strftime('%Y-%m-%d') + datetime.timedelta(days=1))
        except: pass

        data.append({'x': date_output, 'y': temp})

        if min == 0:
            min = date_0

    try: del labels[-1]
    except: pass

    max = date_0

    if scale == 'date':
        while min != max:
            labels.append(min.strftime('%Y-%m-%d'))
            temp = min + datetime.timedelta(days=1)
            min = temp
        labels.append(min.strftime('%Y-%m-%d'))
    else: labels.append(date_output)

    return [labels, data]