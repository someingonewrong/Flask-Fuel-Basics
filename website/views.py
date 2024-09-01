from flask import Blueprint, render_template, request, flash, make_response
from flask_login import login_required, current_user
from . import db
from .database import post_record, get_vehicles, fetch_records, delete_record, sql_query_func, get_date_mileage
from .csv_things import allowed_file, read_csv, csv_setup

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
        if result.startswith('Data'):
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('new_vehicle.html', user=current_user)

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
            if message == 'An error occured somewhere.':
                flash(message, category='error')
            else: flash(message, category='message')
            
        return render_template('import.html', user = current_user)

    return render_template('import.html', user = current_user)

@views.route('/view-records', methods=['GET', 'POST'])
@login_required
def view_records():
    columns = ['id', 'vehicle', 'date', 'mileage', 'litres', 'cost', 'currency', 'user_id', 'date_uploaded']
    vehicles = get_vehicles(current_user)

    vehicle = 'all'
    column = 'id'
    updown = 'DESC'

    if request.method == 'POST' and 'vehicle' in request.form:
        vehicle = request.form.get('vehicle')
        column = request.form.get('column')
        updown = request.form.get('updown')
        table = fetch_records(current_user, vehicle, column, updown)
        
    elif request.method == 'POST' and len(request.form) > 0 and request.form.get('delete') == 'Delete':
        message = delete_record(current_user, request.form)
        flash(message[0], message[1])
        table = fetch_records(current_user)

    elif request.method == 'POST' and len(request.form) > 1 and request.form.get('export') == 'Export':
        file = csv_setup(current_user, request.form)
        table = fetch_records(current_user)
        
        response = make_response(file[1])
        cd = f'attachment; filename={file[0]}'
        response.headers['Content-Disposition'] = cd 
        response.mimetype='text/csv'

        return response
    else:
        table = fetch_records(current_user)
        
    return render_template('view_records.html', 
                           user=current_user, 
                           lines = table, 
                           vehicles = vehicles, 
                           columns = columns, 
                           vehicle = vehicle, 
                           column = column, 
                           updown = updown)

@views.route('/mileage-change', methods=['GET', 'POST'])
@login_required
def mileage_change():
    vehicles = get_vehicles(current_user)
    for x in vehicles:
        vehicle = x
        break

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
    
    data = get_date_mileage(current_user, vehicle)
    
    return render_template('mileage_change.html',
                           user=current_user,
                           vehicle = vehicle,
                           vehicles = vehicles,
                           labels = data[0],
                           values = data[1],
                           all_data = data[2])

@views.route('/sql', methods=['GET', 'POST'])
@login_required
def sql_query():
    if current_user.id == 1:
        if request.method == 'POST':
            result = sql_query_func()
            flash(result[0], result[1])

        return render_template('sql.html', user=current_user)
    return '<h1>Nope</h1>'

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)
