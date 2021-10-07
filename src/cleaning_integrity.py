import numpy as np
import pandas as pd
import utils as utl

def cleaning_global(nrows: int = None) -> pd.DataFrame:
    dtype_dict = {"No voie": "Int64",
                "Code voie": str,
                "Code postal": "Int64",
                "Code department": str,
                "Code Commune": "Int64",
                "Prefixe de section": "Int64",
                "No plan": "Int64",
                "Nombre de lots": "Int64",
                "Code type local": "Int64",
                "Surface reelle bati": "Int64",
                "Nombre pieces principales": "Int64",
                "Nature culture": str,
                "Nature culture speciale": str,
                "Surface terrain": "Int64"}
    if nrows == None:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict)
    else:
        df = pd.read_csv("../data/RAW/valeursfoncieres-2020.txt",
                    sep= "|", parse_dates= ["Date mutation"], dtype = dtype_dict, nrows = nrows)

    str_float_series = ["Valeur fonciere",
                        "Surface Carrez du 1er lot",
                        "Surface Carrez du 2eme lot",
                        "Surface Carrez du 3eme lot",
                        "Surface Carrez du 4eme lot",
                        "Surface Carrez du 5eme lot"]

    df[str_float_series].apply(str_to_float)

    if nrows == None:
        df.to_csv("../data/CURATED/valeursfoncieres-2020.csv")

    return df

def str_to_float(series: pd.Series):
    if len(series[series.notna()]) != 0:
        return series.str.replace(",", ".").astype(float)
