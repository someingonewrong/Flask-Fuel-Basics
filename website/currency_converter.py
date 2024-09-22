import os.path as op
import glob
from currency_converter import CurrencyConverter

def update_ecb_file():
    all_old = op.join('./instance/', '*.zip')

    file_names = glob.glob(all_old, recursive=True)
    file_names.sort(reverse = True)

    for file in file_names:
        c = CurrencyConverter(file, fallback_on_missing_rate=True)
        break

    return c