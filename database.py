from flask import request
import sqlite3

class Record:
    def __init__(self, vehicle, date, mileage, litres, cost, currency):
        self.vehicle = vehicle
        self.date = date
        self.mileage = mileage
        self.litres = litres
        self.cost = cost
        self.currency = currency

    def insert_record(self):
        table_input = "INSERT INTO tracker (vehicle, date, mileage, litres, cost, currency) VALUES (?,?,?,?,?,?)"
        inputs = [self.vehicle, self.date, self.mileage, self.litres, self.cost, self.currency]

        con = db_con()
        con.execute(table_input, inputs)
        db_clo(con)

def db_con():
    return sqlite3.connect("fuel_tracker.db")

def db_clo(con):
    con.commit()

def create_table():
    con = db_con()
    con.execute("""CREATE TABLE IF NOT EXISTS tracker 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                vehicle TEXT, 
                date DATE, 
                mileage INTEGER, 
                litres INTEGER, 
                cost INTEGER, 
                currency TEXT)""")
    db_clo(con)

def get_vehicles():
    try:
        con = db_con()
        query = 'SELECT DISTINCT vehicle FROM tracker'
        vehicles = con.execute(query)
        db_clo(con)
        vehicle_text = []
        for vehic in vehicles:
            vehicle_text.append(vehic[0])
        return vehicle_text
    except Exception as e:
        print('Something is broken. The error: \n' + str(e))
        return []
    
def get_columns():
    try:
        con = db_con()
        query = "SELECT group_concat(name) FROM pragma_table_info('tracker')"  
        columns = list(con.execute(query))[0]
        db_clo(con)
        columns_text = []
        for column in columns[0].split(','):
            columns_text.append(column)
        return columns_text
    except Exception as e:
        print('Something is broken. The error: \n' + str(e))
        return []
    
def get_last_mileage(vehicle):
    try:
        con = db_con()
        query = f"SELECT mileage FROM tracker WHERE vehicle = '{vehicle}' ORDER BY mileage DESC"
        mileage = con.execute(query).fetchone()[0]
        db_clo(con)
        return mileage
    except:
        return 0

def post_record():
    record = Record(request.form.get('vehicle'),
                    request.form.get('date'),
                    request.form.get('mileage'),
                    request.form.get('litres'),
                    request.form.get('cost'),
                    'GBP')

    if len(record.date) != 10:
        print('invalid date')
        pass
    elif len(record.vehicle) < 1:
        print('invalid vehicle')
        pass
    elif len(record.mileage) < 1:
        print('invalid mileage')
        pass
    elif len(record.litres) < 1:
        print('invalid litres')
        pass
    elif len(record.cost) < 1:
        print('invalid cost')
        pass
    else:
        return check_input(record)

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

def check_input(record):
    con = db_con()
    temp = list(con.execute("SELECT DISTINCT vehicle FROM tracker"))
    vehicles = []
    try:
        mileage_last = con.execute("SELECT mileage FROM tracker WHERE vehicle = '{}' ORDER BY mileage DESC LIMIT 1".format(record.vehicle)).fetchone()[0]
    except: pass
    db_clo(con)

    for item in temp:
        vehicles.append(item[0])

    if record.vehicle not in vehicles: return 'invalid vehicle'

    if mileage_last > int(record.mileage):
        return 'Invalid mileage'
    
    try: record.litres = int_convert(record.litres)
    except: return 'Invalid litres'
    
    try: record.cost = int_convert(record.cost)
    except: return 'Invalid cost'

    record.insert_record()
    return 'Success'

def view_records(vehicle = '*', column = 'id', updown = 'ASC'):
    con = db_con()
    if vehicle == '*':
        query = f'SELECT * FROM tracker ORDER BY {column} {updown}'
    else:
        query = f'SELECT * FROM tracker WHERE vehicle = \'{vehicle}\' ORDER BY {column} {updown}'
    table = list(con.execute(query))
    db_clo(con)
    return table

def sql_query_func():
    con = db_con()
    try:
        con.execute(request.form.get('sql_line'))
        db_clo(con)
        return 'success'
    except:
        db_clo(con)
        return 'failed'