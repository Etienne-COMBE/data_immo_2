import pandas as pd

def data_import_integrity(nrows: int = None) -> pd.DataFrame:
    dtype_dict = {
                "Code voie": str,
                "Code department": str,
                "Nature culture": str,
                "Nature culture speciale": str}
    if nrows == None:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict)
    else:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict, nrows = nrows)

    df.columns = df.columns.str.replace(" ", "_")

    str_float_series = ["Valeur_fonciere",
                        "Surface_Carrez_du_1er_lot",
                        "Surface_Carrez_du_2eme_lot",
                        "Surface_Carrez_du_3eme lot",
                        "Surface_Carrez_du_4eme lot",
                        "Surface_Carrez_du_5eme lot"]

    df[str_float_series].apply(str_to_float)

    if nrows == None:
        df.to_csv("../data/CURATED/valeursfoncieres-2020.csv")

    return df

def float_to_str(series: pd.Series):
    return series.astype(int).astype(str)

def str_to_float(series: pd.Series):
    if len(series[series.notna()]) != 0:
        return series.str.replace(",", ".").astype(float)

"""
["No voie",
"Code postal",
"Code Commune",
"Prefixe de section",
"No plan",
"Nombre de lots",
"Code type local",
"Surface reelle bati",
"Nombre pieces principales",
"Surface terrain"]
"""