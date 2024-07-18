import database
from flask import Flask, render_template, request, flash
from flask_basicauth import BasicAuth

app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = 'username'
# app.config['BASIC_AUTH_PASSWORD'] = 'password'
# app.config['BASIC_AUTH_FORCE'] = False
app.secret_key = "don't_look_at_me"

# basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-record', methods=['GET', 'POST'])
# @basic_auth.required
def add_record():
    if request.method == 'POST':
        result = database.post_record()
        if result[0] == 'Data Added: ':
            flash(result, category='message')
        else:
            flash(result, category='error')

    vehicles = database.get_vehicles()

    return render_template('add_record.html', vehicles = vehicles)

@app.route('/new-vehicle', methods=['GET', 'POST'])
# @basic_auth.required
def new_vehicle():
    if request.method == 'POST':
        result = database.post_record()
        if result[0] == 'Data Added: ':
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('new_vehicle.html')

@app.route('/view-records', methods=['GET', 'POST'])
# @basic_auth.required
def view_records():
    columns = database.get_columns()
    vehicles = database.get_vehicles()

    if request.method == 'POST':
        vehicle = request.form.get('vehicle')
        column = request.form.get('column')
        updown = request.form.get('updown')
        table = database.view_records(vehicle, column, updown)
        return render_template('view_records.html', lines = table, vehicles = vehicles, columns = columns, vehicle = vehicle, column = column, updown = updown)
    else:
        table = database.view_records()
        return render_template('view_records.html', lines = table, vehicles = vehicles, columns = columns, vehicle = 'all', column = 'id', updown = 'ASC')

@app.route('/sql', methods=['GET', 'POST'])
# @basic_auth.required
def sql_query():
    if request.method == 'POST':
        result = database.sql_query_func()
        if result[0] == 'sql success':
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('sql.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    database.create_table()
    app.run(debug=True)


