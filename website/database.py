from flask import request
from .models import Record
from . import db
from datetime import date
import sqlite3
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
    try: date_convert = date(int(date_test[0]), int(date_test[1]), int(date_test[2]))
    except: date_convert = date.today()

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

    mileage_last = sorted(mileages_useable)[-1]

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

def fetch_records(current_user, vehicle = '*', column = 'id', updown = 'ASC'):
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
        

def sql_query_func(): # It don't work :( not sure how to fix. always get 'unable to open database file'
    try:
        path_ = path.dirname(path.abspath(__file__))
        db_path = path.join(path_.strip('website/'), 'instance/fuel_tracker_backup.db')
        con = sqlite3.connect(db_path)
        result = con.execute(request.form.get('sql_line'))
        con.commit()
        con.close()
        print(list(result))
        return ['sql success', 'message']
    except Exception as e:
        print(e)
        return ['sql failed', 'error']
    
def get_date_mileage(current_user, vehicle):
    all_data = Record.query.filter(Record.user_id == current_user.id, Record.vehicle == vehicle).all()
    labels = []
    values = []

    for line in all_data:
        labels.append(str(line.date))
        values.append(str(line.mileage))
    
    return [labels, values]