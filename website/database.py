from flask import request
# from flask_sqlalchemy import SQLAlchemy
from .models import Record
from . import db
from datetime import date

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
    
def get_columns():
    try:
        con = db_con()
        query = "SELECT group_concat(name) FROM pragma_table_info('tracker')"  
        columns = list(con.execute(query))[0]
        con.commit()
        columns_text = []
        for column in columns[0].split(','):
            columns_text.append(column)
        return columns_text
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

def check_input(record, vehicles, current_user):
    url = str(request.base_url.split('/')[-1])
    error_message = ''
    mileages = Record.query.filter_by(user_id = current_user.id).filter_by(vehicle = record.vehicle)
    mileages_useable = []

    for mileage in mileages:
        mileages_useable.append(mileage.mileage)

    mileage_last = sorted(mileages_useable, reverse=True)[0]

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

def view_records(vehicle = '*', column = 'id', updown = 'ASC'):
    if vehicle == '*':
        query = f'SELECT * FROM tracker ORDER BY {column} {updown}'
    else:
        query = f'SELECT * FROM tracker WHERE vehicle = \'{vehicle}\' ORDER BY {column} {updown}'
    # table = list(con.execute(query))
    # con.commit()
    # return table

def sql_query_func():
    try:
        # result = con.execute(request.form.get('sql_line'))
        # con.commit()
        # print(list(result))
        return ['sql success']
    except:
        # con.commit()
        return ['sql failed']