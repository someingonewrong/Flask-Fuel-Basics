from .currency_converter import update_ecb_file
from .inflation_converter import inflation_convert
from .database import fetch_records
import datetime

def get_date_mileage(current_user, vehicle, scale):
    all_data = fetch_records(current_user, vehicle)
    labels = []
    data = []
    date = 0
    min = 0
    max = 0

    for line in all_data:
        date = datetime.datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        data.append({"x": date_output, "y": int(line.mileage)})

        if scale == 'instance':
            labels.append(date_output)

        if min == 0:
            min = date

    max = date

    if scale == 'date':
        while min != max:
            labels.append(min.strftime('%Y-%m-%d'))
            temp = min + datetime.timedelta(days=1)
            min = temp
        labels.append(date_output)

    return [labels, data]

def get_per_fill(current_user, vehicle, scale, smoothing):
    all_data = fetch_records(current_user, vehicle)
    labels = []
    data = []
    date = 0
    min = 0
    max = 0
    mileage = []
    mileage_change = 0

    for line in all_data:
        date = datetime.datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        mileage.append(int(line.mileage))

        if int(smoothing) == 1:
            try: mileage_change = int(mileage[-1]) - int(mileage[-2])
            except: pass
        elif int(smoothing) == 3:
            try: mileage_change = (int(mileage[-1]) - int(mileage[-4])) / 3
            except: 
                try: mileage_change = (int(mileage[-1]) - int(mileage[-3])) / 2
                except: 
                    try: mileage_change = int(mileage[-1]) - int(mileage[-2])
                    except: pass
        elif int(smoothing) == 5:
            try: mileage_change = (int(mileage[-1]) - int(mileage[-6])) / 5
            except:
                try: mileage_change = (int(mileage[-1]) - int(mileage[-5])) / 4
                except:
                    try: mileage_change = (int(mileage[-1]) - int(mileage[-4])) / 3
                    except: 
                        try: mileage_change = (int(mileage[-1]) - int(mileage[-3])) / 2
                        except: 
                            try: mileage_change = int(mileage[-1]) - int(mileage[-2])
                            except: pass

        print(mileage_change)

        data.append({"x": date_output, "y": mileage_change})

        if scale == 'instance':
            labels.append(date_output)

        if min == 0:
            min = date

    print(mileage)

    max = date

    if scale == 'date':
        while min != max:
            labels.append(min.strftime('%Y-%m-%d'))
            temp = min + datetime.timedelta(days=1)
            min = temp
        labels.append(date_output)

    return [labels, data]

def get_fuel_cost(current_user, vehicle, scale, currency_con, inflation_con):
    all_data = fetch_records(current_user, vehicle)
    labels = []
    data = []
    temp = 1.5
    min = 0
    max = 0

    if currency_con == 'Y':
        c = update_ecb_file()

    for line in all_data:
        date_0 = datetime.datetime.strptime(str(line.date), '%Y-%m-%d')
        date_1 = date_0 + datetime.timedelta(days=1)
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
                    date_output = str(date_1.strftime('%Y-%m-%d') + datetime.timedelta(days=1))
        except: pass

        data.append({'x': date_output, 'y': temp, 'currency': line.currency})

        if min == 0:
            min = date_0

    try: del labels[-1]
    except: pass

    max = date_0

    if scale == 'date':
        while min != max:
            labels.append(min.strftime('%Y-%m-%d'))
            temp = min + datetime.timedelta(days=1)
            min = temp
        labels.append(min.strftime('%Y-%m-%d'))
    else: labels.append(date_output)

    if inflation_con == 'Y':
        data = inflation_convert(data, currency_con)

    return [labels, data]