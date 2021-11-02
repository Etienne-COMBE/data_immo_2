import pandas as pd

import cleaning_integrity as cln_int
import clean_df_ziad as cln_z

def cleaning_global(nrows:int = None):
    df = cln_int.data_import_integrity(nrows)

    df["Code_id_commune"] = df["Code_commune"].values + df["Commune"].values + df["Code_departement"].values
    df["Code_id_commune"] = df["Code_id_commune"].astype("category").cat.codes.astype("int64")

    df = cln_z.clean_na(df)
    print("Impute 0")
    df = cln_int.data_imputation(df)
    print("Impute by Code_id_commune")
    df = cln_int.to_int(df)

    df = df.drop_duplicates()
    cln_int.data_export(df)
    return df
