from .currency_converter import update_ecb_file
from .inflation_converter import inflation_convert
from .database import fetch_records_graph
from .smoothing import mileage_one, mileage_three, mileage_five, mileage_all, mpg_one, mpg_three, mpg_five, mpg_all
from datetime import datetime
from datetime import timedelta

def get_date_mileage(current_user, vehicle, scale):
    all_data = fetch_records_graph(current_user, vehicle)
    labels = []
    data = []
    min = 0
    max = 0

    for line in all_data:
        date_output = str(line.date)
        data.append({"x": date_output, "y": int(line.mileage)})

        if scale == 'instance':
            labels.append(date_output)

    if scale == 'date':
        labels = get_labels(min, max, data)

    return [labels, data]

def get_per_fill(current_user, vehicle, scale, smoothing):
    all_data = fetch_records_graph(current_user, vehicle)
    labels = []
    data = []
    data3 = []
    data5 = []
    min = 0
    max = 0
    mileage = []
    mileage_change = 0

    for line in all_data:
        date_output = str(line.date)
        mileage.append(int(line.mileage))

        if smoothing == '3':
            mileage_change = mileage_three(mileage)
        elif smoothing == '5':
            mileage_change = mileage_five(mileage)
        else:
            mileage_change = mileage_one(mileage)

        data.append({"x": date_output, "y": mileage_change})

        if scale == 'instance':
            labels.append(date_output)

    data.pop(0)

    if smoothing == 'all':
        data3 = mileage_all(all_data, 3)
        data3.pop(0)
        data5 = mileage_all(all_data, 5)
        data5.pop(0)

    if scale == 'date':
        labels = get_labels(min, max, data)
    else:
        labels.pop(0)

    return [labels, data, data3, data5]

def get_MPG(current_user, vehicle, scale, smoothing):
    all_data = fetch_records_graph(current_user, vehicle)
    labels = []
    data = []
    data3 = []
    data5 = []
    min = 0
    max = 0
    mileage = []
    litres = []
    mpg = 0

    for line in all_data:
        date_output = str(line.date)
        mileage.append(int(line.mileage))
        litres.append(int(line.litres))

        if smoothing == '3':
            mpg = mpg_three(mileage, litres)
        elif smoothing == '5':
            mpg = mpg_five(mileage, litres)
        else:
            mpg = mpg_one(mileage, litres)

        data.append({"x": date_output, "y": mpg})

        if scale == 'instance':
            labels.append(date_output)

    data.pop(0)

    if smoothing == 'all':
        data3 = mpg_all(all_data, 3)
        data3.pop(0)
        data5 = mpg_all(all_data, 5)
        data5.pop(0)

    if scale == 'date':
        labels = get_labels(min, max, data)
    else:
        labels.pop(0)

    return [labels, data, data3, data5]

def get_fuel_cost(current_user, vehicle, scale, currency_con, inflation_con):
    all_data = fetch_records_graph(current_user, vehicle)
    labels = []
    data = []
    temp = 1.5
    min = 0
    max = 0

    if currency_con == 'Y' or inflation_con == 'Y':
        c = update_ecb_file()
        currency_con = 'Y'

    for line in all_data:
        date_1 = datetime.strptime(str(line.date), '%Y-%m-%d') + timedelta(days=1)
        date_output = str(line.date)
        try: 
            if int(line.cost)/(int(line.litres)) != 0:
                try:
                    if currency_con == 'Y':
                        line.cost = c.convert(int(line.cost), line.currency, 'GBP', date=line.date)
                except Exception as e: print(e)
                temp = "%.2f" % (int(line.cost)/int(line.litres))
        except: pass

        if scale == 'instance':
            labels.append(date_output)

        try:
            if labels[-1] == labels[-2]:
                date_output = str(date_1.strftime('%Y-%m-%d'))
                if date_output == labels[-2]:
                    date_output = str(date_1.strftime('%Y-%m-%d') + timedelta(days=1))
        except: pass

        data.append({'x': date_output, 'y': temp, 'currency': line.currency})

    try: del labels[-1]
    except: pass

    if scale == 'date':
        labels = get_labels(min, max, data)
    else: labels.append(date_output)

    if inflation_con == 'Y':
        data = inflation_convert(data)

    return [labels, data]

def get_labels(min, max, data):
    labels = []
    min = datetime.strptime(data[0]['x'], '%Y-%m-%d')
    max = datetime.strptime(data[-1]['x'], '%Y-%m-%d')
    while min != max:
        labels.append(min.strftime('%Y-%m-%d'))
        temp = min + timedelta(days=1)
        min = temp
    labels.append(min.strftime('%Y-%m-%d'))
    return labels