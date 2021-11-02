import pandas as pd
import dask.dataframe as dd

def data_import_integrity(nrows: int = None) -> pd.DataFrame:
    dtype_dict = {
                "Code voie": str,
                "Code department": str,
                "Nature culture": str,
                "Nature culture speciale": str,
                "No voie": str,
                "Code type local": str,
                "Prefixe de section": str,
                "No disposition": str,
                "Code commune": str,
                "Code departement": str,
                "No plan": str,
                '1er lot': 'object',
                '2eme lot': 'object',
                '3eme lot': 'object',
                'No Volume': 'object',
                'Surface Carrez du 5eme lot': 'object'}
    if nrows == None:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict)
    else:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict, nrows = nrows)
    print("Import")
    df.columns = df.columns.str.replace(" ", "_")

    df["No_disposition"] = df["No_disposition"].str.strip("0")
    
    df = str_to_float(df)
    df = code_postal_str(df)

    return df

def str_to_float(df):
    str_float_features = ["Valeur_fonciere",
                        "Surface_Carrez_du_1er_lot",
                        "Surface_Carrez_du_2eme_lot",
                        "Surface_Carrez_du_3eme_lot",
                        "Surface_Carrez_du_4eme_lot",
                        "Surface_Carrez_du_5eme_lot"]
    
    df[str_float_features] = df[str_float_features].apply(lambda x: x.str.replace(",", ".").astype(float))
    print("Integrity")
    return df

def code_postal_str(df):
    str_code = df.Code_postal.astype(str).str[:-2].copy()
    df["Code_postal"] = pd.concat(['0' + str_code[str_code.str.len() == 4], str_code[str_code.str.len() == 5]])
    return df

#-----------------------#
# To use in cleaning.py #
#-----------------------#


def to_int(df):
    int_features = ["Nombre_de_lots",
                    "Nombre_pieces_principales",
                    "Surface_reelle_bati",
                    "Surface_terrain"]
    df[int_features] = df[int_features].astype(int)
    return df



def data_export(df, nrows: int= None):
    if nrows == None:
        df.to_csv("../data/CURATED/valeursfoncieres-2020.csv", index = False)

def data_imputation(df: pd.DataFrame):
    df["Section"] = df.groupby("Code_id_commune").Section.transform(lambda x: x.fillna(x.mode()[0]))
    df.dropna(axis = 0, how = "any", inplace = True)
    return df
