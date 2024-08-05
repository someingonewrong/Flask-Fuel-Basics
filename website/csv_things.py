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
        if request.form.get('key') == 'key':
            reader = csv.DictReader(text_file, delimiter=',')
        else: reader = csv.reader(text_file, delimiter=',')

        vehicle = file.filename.rsplit('.', 1)[0].lower()

        for line in reader:
            temp_date = line[0].split('/')
            line_date = date(int(temp_date[2])+2000, int(temp_date[1]), int(temp_date[1]))
            line_mileage = int(line[1])
            line_cost = int_convert(line[2])
            line_litres = int_convert(line[3])

            record = Record(vehicle = vehicle,
                    date = line_date,
                    mileage = line_mileage,
                    litres = line_litres,
                    cost = line_cost,
                    currency = 'GBP',
                    user_id = current_user.id)
            
            db.session.add(record)

        db.session.commit()

    return 'added them all'