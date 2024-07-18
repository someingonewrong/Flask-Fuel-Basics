from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Record
from . import db
import json
from .database import post_record, get_vehicles, get_columns, sql_query_func, view_records

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
    # columns = database.get_columns()
    # vehicles = database.get_vehicles()

    # if request.method == 'POST':
    #     vehicle = request.form.get('vehicle')
    #     column = request.form.get('column')
    #     updown = request.form.get('updown')
    #     table = database.view_records(vehicle, column, updown)
    #     return render_template('view_records.html', lines = table, vehicles = vehicles, columns = columns, vehicle = vehicle, column = column, updown = updown)
    # else:
    #     table = database.view_records()
    #     return render_template('view_records.html', lines = table, vehicles = vehicles, columns = columns, vehicle = 'all', column = 'id', updown = 'ASC')
    return '<h1>not ready yet</h1>'

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