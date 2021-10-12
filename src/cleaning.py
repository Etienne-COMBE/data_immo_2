import pandas as pd

import cleaning_integrity as cln_int
import clean_df_ziad as cln_z

def cleaning_global():
    df = cln_int.data_import_integrity()
    df = cln_z.clean_na(df)
    df = cln_z.fill_code_postal(df)
    df = cln_int.to_int(df)
    cln_int.data_export(df)
    return df
