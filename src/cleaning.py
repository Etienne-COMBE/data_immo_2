import pandas as pd

from cleaning_integrity import data_import_integrity

def cleaning_global():
    df = data_import_integrity()
    return df