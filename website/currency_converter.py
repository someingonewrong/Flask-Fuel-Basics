from datetime import date
from datetime import datetime
from datetime import timedelta
import os.path as op
from os import remove
import glob
import urllib.request
from currency_converter import ECB_URL, CurrencyConverter

def fetch_ecb_file(filename):
    print('\nUpdating converter file...')
    try:
        urllib.request.urlretrieve(ECB_URL, filename)
        print('File updated')
    except: raise

def update_ecb_file():
    if date.today().weekday() in [0,1,2,3,4]:
        temp = datetime.today()
    elif date.today().weekday() == 5:
        temp = datetime.today() - timedelta(days=1)
    else:
        temp = datetime.today() - timedelta(days=2)
    temp = temp.strftime('%Y%m%d')
    filename = str(temp) + ".zip"
    
    try:
        if not op.isfile(filename):
            fetch_ecb_file(str(temp) + ".zip")
    except:
        print('Failed to update file')
    
    file_names = glob.glob('*.zip', recursive=True)
    file_names.sort(reverse = True)

    for file in file_names:
        try:
            c = CurrencyConverter(fallback_on_missing_rate=True)
            print('Loaded file ' + file)
            break
        except: print('broken')

    for file_delete in file_names:
        if file_delete != file:
            remove(file_delete)
    
    return c