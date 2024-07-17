import database
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "don't_look_at_me"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-record', methods=['GET', 'POST'])
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
def new_vehicle():
    if request.method == 'POST':
        result = database.post_record()
        if result[0] == 'Data Added: ':
            flash(result, category='message')
        else:
            flash(result, category='error')

    return render_template('new_vehicle.html')

@app.route('/view-records', methods=['GET', 'POST'])
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


