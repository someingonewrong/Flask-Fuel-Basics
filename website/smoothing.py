from datetime import datetime

def one(mileage):
    try: mileage_change = int(mileage[-1]) - int(mileage[-2])
    except: mileage_change = 0
    return mileage_change

def three(mileage):
    try: mileage_change = (int(mileage[-1]) - int(mileage[-4])) / 3
    except: 
        try: mileage_change = (int(mileage[-1]) - int(mileage[-3])) / 2
        except: 
            mileage_change = one(mileage)
    return mileage_change

def five(mileage):
    try: mileage_change = (int(mileage[-1]) - int(mileage[-6])) / 5
    except:
        try: mileage_change = (int(mileage[-1]) - int(mileage[-5])) / 4
        except:
            mileage_change = three(mileage)
    return mileage_change

def all(all_data, smoothing):
    mileage = []
    data = []
    for line in all_data:
        date = datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        mileage.append(int(line.mileage))

        if smoothing == 3:
            mileage_change = three(mileage)
        else:
            mileage_change = five(mileage)

        data.append({"x": date_output, "y": mileage_change})
    return data
