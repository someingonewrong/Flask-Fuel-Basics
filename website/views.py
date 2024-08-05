from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .database import post_record, get_vehicles, fetch_records
from .csv_things import allowed_file, read_csv # download_csv, 

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/add-record', methods=['GET', 'POST'])
@login_required
def add_record():
    vehicles = get_vehicles(current_user)

    if request.method == 'POST':
        result = post_record(current_user, vehicles)
        if result.startswith('Data'):
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('add_record.html', user=current_user, vehicles = vehicles)

@views.route('/new-vehicle', methods=['GET', 'POST'])
@login_required
def new_vehicle():
    if request.method == 'POST':
        result = post_record(current_user)
        if result == 'success':
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('new_vehicle.html', user=current_user)

@views.route('/view-records', methods=['GET', 'POST'])
@login_required
def view_records():
    columns = ['id', 'vehicle', 'date', 'mileage', 'litres', 'cost', 'currency', 'user_id', 'date_uploaded']
    vehicles = get_vehicles(current_user)

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        column = request.form.get('column')
        updown = request.form.get('updown')
        table = fetch_records(current_user, vehicle, column, updown)
        return render_template('view_records.html', user=current_user, lines = table, vehicles = vehicles, columns = columns, vehicle = vehicle, column = column, updown = updown)
    else:
        table = fetch_records(current_user)
        return render_template('view_records.html', user=current_user, lines = table, vehicles = vehicles, columns = columns, vehicle = 'all', column = 'id', updown = 'ASC')

@views.route('/import-csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return render_template('import.html', user = current_user)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', category='error')
            return render_template('import.html', user = current_user)
        
        if file and allowed_file(file.filename):
            message = read_csv(file, current_user)
            flash(message, category='message')
        return render_template('import.html', user = current_user)

    return render_template('import.html', user = current_user)

@views.route('/sql', methods=['GET', 'POST'])
@login_required
def sql_query():
    # if request.method == 'POST':
    #     result = database.sql_query_func()
    #     if result[0] == 'sql success':
    #         flash(result, category='message')
    #     else:
    #         flash(result, category='error')

    return render_template('sql.html', user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)


# import sqlite3
# from .models import Record
# from datetime import date

# @views.route('/export_import')
# @login_required
# def export_import():
#     con = sqlite3.connect("website/fuel_tracker.db")  #connect to the database
#     cursor = con.cursor()

#     all_records = list(cursor.execute('SELECT * FROM tracker'))

#     for line in all_records:
#         date_test = line[2].split('-')
#         date_convert = date(int(date_test[0]), int(date_test[1]), int(date_test[2]))
#         record = Record(vehicle = line[1],
#                     date = date_convert,
#                     mileage = line[3],
#                     litres = line[4],
#                     cost = line[5],
#                     currency = line[6],
#                     user_id = current_user.id)
#         db.session.add(record)
#         db.session.commit()

#     con.commit()
#     con.close()
#     return ('read')