from flask import request
from .models import Record
from . import db
from datetime import date
import csv
import io
from .database import int_convert

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv(file, current_user):
    
    with io.TextIOWrapper(file, encoding='utf-8') as text_file:

        vehicle = file.filename.rsplit('.', 1)[0].lower()

        try:
            if request.form.get('key') == 'key':
                line_n = dict_csv(text_file, current_user, vehicle)
            else:
                line_n = row_csv(text_file, current_user, vehicle)

            db.session.commit()
            message = 'Added ' + str(line_n) + ' Rows'
        except:
            message = 'An error occured somewhere.'

    return message

def row_csv(text_file, current_user, vehicle):
    reader = csv.reader(text_file, delimiter=',')

    line_n = 0

    for line in reader:
        line_n += 1
        temp_date = line[0].split('/')
        line_date = date(int(temp_date[2])+2000, int(temp_date[1]), int(temp_date[1]))
        line_mileage = int(line[1].strip('p'))
        line_cost = int_convert(line[2])
        line_litres = int_convert(line[3])
        try: currency = line[4]
        except: currency = 'GBP'

        record = Record(vehicle = vehicle,
                date = line_date,
                mileage = line_mileage,
                litres = line_litres,
                cost = line_cost,
                currency = currency,
                user_id = current_user.id)
                
        db.session.add(record)
    
    return line_n

def dict_csv(text_file, current_user, vehicle):
    reader = csv.DictReader(text_file, delimiter=',')

    line_n = 0

    for line in reader:
        line_n += 1
        try: line_vehicle = line['vehicle']
        except: line_vehicle = vehicle
        temp_date = line['date'].split('/')
        line_date = date(int(temp_date[2])+2000, int(temp_date[1]), int(temp_date[1]))
        line_mileage = int(line['mileage'])
        line_cost = int_convert(line['cost'])
        line_litres = int_convert(line['litres'])
        try: currency = line['currency']
        except: currency = 'GBP'

        record = Record(vehicle = line_vehicle,
                date = line_date,
                mileage = line_mileage,
                litres = line_litres,
                cost = line_cost,
                currency = currency,
                user_id = current_user.id)
            
        db.session.add(record)

    db.session.commit()

    return line_n