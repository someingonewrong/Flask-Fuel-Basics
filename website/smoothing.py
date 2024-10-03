from datetime import datetime

def mileage_one(mileage):
    try: mileage_change = int(mileage[-1]) - int(mileage[-2])
    except: mileage_change = 0
    return mileage_change

def mileage_three(mileage):
    try: mileage_change = (int(mileage[-1]) - int(mileage[-4])) / 3
    except: 
        try: mileage_change = (int(mileage[-1]) - int(mileage[-3])) / 2
        except: 
            mileage_change = mileage_one(mileage)
    return mileage_change

def mileage_five(mileage):
    try: mileage_change = (int(mileage[-1]) - int(mileage[-6])) / 5
    except:
        try: mileage_change = (int(mileage[-1]) - int(mileage[-5])) / 4
        except:
            mileage_change = mileage_three(mileage)
    return mileage_change

def mileage_all(all_data, smoothing):
    mileage = []
    data = []
    for line in all_data:
        date = datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        mileage.append(int(line.mileage))

        if smoothing == 3:
            mileage_change = mileage_three(mileage)
        else:
            mileage_change = mileage_five(mileage)

        data.append({"x": date_output, "y": mileage_change})
    return data

def mpg_one(mileage, litres):
    try:
        mileage_change = int(mileage[-1]) - int(mileage[-2])
        mpg = mileage_change / (litres[-1] * 0.002199692483)
    except: mpg = 0
    return round(mpg,1)

def mpg_three(mileage, litres):
    try: 
        mileage_change = (int(mileage[-1]) - int(mileage[-4]))
        mpg = mileage_change / ((litres[-1] + litres[-2] + litres[-3]) * 0.002199692483)
    except: 
        try: 
            mileage_change = (int(mileage[-1]) - int(mileage[-3]))
            mpg = mileage_change / ((litres[-1] + litres[-2]) * 0.002199692483)
        except: 
            mpg = mpg_one(mileage, litres)
    return round(mpg,1)

def mpg_five(mileage, litres):
    try: 
        mileage_change = (int(mileage[-1]) - int(mileage[-6]))
        mpg = mileage_change / ((litres[-1] + litres[-2] + litres[-3] + litres[-4] + litres[-5]) * 0.002199692483)
    except:
        try: 
            mileage_change = (int(mileage[-1]) - int(mileage[-5]))
            mpg = mileage_change / ((litres[-1] + litres[-2] + litres[-3] + litres[-4]) * 0.002199692483)
        except:
            mpg = mpg_three(mileage, litres)
    return round(mpg,1)

def mpg_all(all_data, smoothing):
    mileage = []
    litres = []
    data = []
    for line in all_data:
        date = datetime.strptime(str(line.date), '%Y-%m-%d')
        date_output = str(date.strftime('%Y-%m-%d'))
        mileage.append(int(line.mileage))
        litres.append(int(line.litres))

        if smoothing == 3:
            mpg = mpg_three(mileage, litres)
        else:
            mpg = mpg_five(mileage, litres)

        data.append({"x": date_output, "y": mpg})
    return data