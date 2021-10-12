import pandas as pd

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
                "No plan": str}
    if nrows == None:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict)
    else:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict, nrows = nrows)

    df.columns = df.columns.str.replace(" ", "_")

    df["No_disposition"] = df["No_disposition"].str.strip("0")
    str_float_features = ["Valeur_fonciere",
                        "Surface_Carrez_du_1er_lot",
                        "Surface_Carrez_du_2eme_lot",
                        "Surface_Carrez_du_3eme_lot",
                        "Surface_Carrez_du_4eme_lot",
                        "Surface_Carrez_du_5eme_lot"]
    df[str_float_features] = df[str_float_features].apply(str_to_float)
    df["Code_postal"] = code_postal_str(df["Code_postal"])

    return df

def str_to_float(series: pd.Series):
    if len(series[series.notna()]) != 0:
        series = series.str.replace(",", ".").astype(float)
        return series

#-----------------------#
# To use in cleaning.py #
#-----------------------#

def code_postal_str(series: pd.Series) -> pd.Series:
    str_code = series.astype(str).str[:-2].copy()
    series = pd.concat(['0' + str_code[str_code.str.len() == 4], str_code[str_code.str.len() == 5]])
    return series

def to_int(df: pd.DataFrame) -> pd.DataFrame:
    int_features = ["Nombre_de_lots",
                    "Nombre_pieces_principales",
                    "Surface_reelle_bati",
                    "Surface_terrain"]
    df[int_features].astype(int)
    return df

def data_export(df, nrows: int= None):
    if nrows == None:
        df.to_csv("../data/CURATED/valeursfoncieres-2020.csv")
