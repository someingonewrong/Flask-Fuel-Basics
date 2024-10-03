from flask import Blueprint, render_template, request, flash, make_response
from flask_login import login_required, current_user
from .database import post_record, get_vehicles, fetch_records, delete_record, has_foreign_currency
from .graphing import get_date_mileage, get_fuel_cost, get_per_fill, get_MPG
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

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        column = request.form.get('column')
        updown = request.form.get('updown')
        if 'vehicle' in request.form:
            table = fetch_records(current_user, vehicle=vehicle, column=column, updown=updown)
    else:
        table = fetch_records(current_user, '*', 'id', 'DESC')
        
    if request.method == 'POST' and len(request.form) > 0 and request.form.get('delete') == 'Delete':
        message = delete_record(current_user, request.form)
        flash(message[0], message[1])
        table = fetch_records(current_user, vehicle, column, updown)

    elif request.method == 'POST' and len(request.form) > 1 and request.form.get('export') == 'Export':
        file = csv_setup(current_user, request.form)
        table = fetch_records(current_user, vehicle, column, updown)
        
        response = make_response(file[1])
        cd = f'attachment; filename={file[0]}'
        response.headers['Content-Disposition'] = cd 
        response.mimetype='text/csv'

        return response
        
    return render_template('view_records.html', 
                           user=current_user, 
                           lines = table, 
                           vehicles = vehicles, 
                           columns = columns, 
                           vehicle = vehicle, 
                           column = column, 
                           updown = updown)

@views.route('/mileage-change-over-time', methods=['GET', 'POST'])
@login_required
def mileage_change_over_time():
    vehicles = get_vehicles(current_user)
    for x in vehicles:
        vehicle = x
        break

    scale = 'date'

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        scale = request.form.get('xScale')
    
    data = get_date_mileage(current_user, vehicle, scale)
    
    return render_template('mileage_change_over_time.html',
                           user=current_user,
                           vehicle = vehicle,
                           vehicles = vehicles,
                           scale = scale,
                           labels = data[0],
                           all_data = data[1])

@views.route('/mileage-per-fill', methods=['GET', 'POST'])
@login_required
def mileage_per_fill():
    vehicles = get_vehicles(current_user)
    for x in vehicles:
        vehicle = x
        break

    scale = 'instance'
    smoothing = '1'

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        scale = request.form.get('xScale')
        smoothing = request.form.get('smoothing')
    
    data = get_per_fill(current_user, vehicle, scale, smoothing)
    
    return render_template('mileage_per_fill.html',
                           user=current_user,
                           vehicle = vehicle,
                           vehicles = vehicles,
                           scale = scale,
                           smoothing = smoothing,
                           labels = data[0],
                           data = data[1],
                           data3 = data[2],
                           data5 = data[3])

@views.route('/mpg-calculator', methods=['GET', 'POST'])
@login_required
def mpg_calculator():
    vehicles = get_vehicles(current_user)
    for x in vehicles:
        vehicle = x
        break

    scale = 'instance'
    smoothing = '1'

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        scale = request.form.get('xScale')
        smoothing = request.form.get('smoothing')
    
    data = get_MPG(current_user, vehicle, scale, smoothing)
    
    return render_template('mileage_per_fill.html',
                           user=current_user,
                           vehicle = vehicle,
                           vehicles = vehicles,
                           scale = scale,
                           smoothing = smoothing,
                           labels = data[0],
                           data = data[1],
                           data3 = data[2],
                           data5 = data[3])

@views.route('/fuel-cost', methods=['GET', 'POST'])
@login_required
def fuel_cost():
    vehicles = get_vehicles(current_user)
    
    for x in vehicles:
        vehicle = x
        break

    scale = 'date'
    currency_con = 'N'
    inflation_con = 'N'

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        scale = request.form.get('xScale')
        try: currency_con = request.form.get('currencyCon')
        except: currency_con = 'N'
        inflation_con = request.form.get('inflationCon')
    
    foreign_currency = has_foreign_currency(current_user, vehicle)

    data = get_fuel_cost(current_user, vehicle, scale, currency_con, inflation_con)
    
    return render_template('fuel_cost.html',
                           user=current_user,
                           vehicle = vehicle,
                           vehicles = vehicles,
                           scale = scale,
                           currency_con = currency_con,
                           foreign_currency = foreign_currency,
                           inflation_con = 'N',
                           labels = data[0],
                           all_data = data[1])

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)
