# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:01:59 2021

@author: ziadh
"""
# data source : https://www.data.gouv.fr/fr/datasets/5c4ae55a634f4117716d5656/
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


FILENAME = "../data/RAW/valeursfoncieres-2020.txt"
df = pd.read_csv(FILENAME,'|')
df.columns = df.columns.str.replace(" ", "_")

def Clean_df(df : pd.DataFrame) -> pd.DataFrame:
    percent_data = df.notnull().sum() * 100 / len(df)
    plt.figure()
    plt.barh(percent_data.index,percent_data)
    plt.xlabel("Percentage of data in columns")
    ''' 
    les colonnes avec un pourcentage de donnée inférieur à 35 sera éliminé 
    L'étude est effectué par commune -> par besoin de no voie et type de voie
    '''
    
    df_s = df.drop(percent_data.index[percent_data < 35], axis=1)
    percent_data_s = df_s.notnull().sum() * 100 / len(df_s)
    plt.figure()
    plt.barh(percent_data_s.index,percent_data_s)
    plt.xlabel("Percentage of data in columns")
    
    df_fill = clean_na(df_s)
    
    percent_data_fill = df_fill.notnull().sum() * 100 / len(df_fill)
    plt.figure()
    plt.barh(percent_data_fill.index,percent_data_fill)
    plt.xlabel("Percentage of data in columns")
    
    df_fill = fill_code_postal(df_fill)

    return df_fill

def Verif_local(df : pd.DataFrame) -> bool:
    # check if type local and code local are correct in my database
    df.duplicated(subset=['Type_local','Code_type_local'], keep="first").sum()
    #df[~df.duplicated(subset=['Type local','Code type local'], keep="first")]
    if len(df) == len(df['Type_local'].unique()) + df.duplicated(subset=['Type_local','Code_type_local'], keep="first").sum():
        return True
    return False

def clean_na(df : pd.DataFrame) -> pd.DataFrame:
    percent_data = df.notnull().sum() * 100 / len(df)
    df_s = df.drop(percent_data.index[percent_data < 35], axis=1)
    df_fill = df_s.copy()
    df_fill["Code_type_local"] = df_fill["Code_type_local"].fillna(0)
    df_fill["Type_local"] = df_fill["Type_local"].fillna("nothing")
    df_fill["Surface_reelle_bati"] = df_fill["Surface_reelle_bati"].fillna(0)
    df_fill["Nombre_pieces_principales"] = df_fill["Nombre_pieces_principales"].fillna(0)
    df_fill["Surface_terrain"] = df_fill["Surface_terrain"].fillna(0)
    df_fill = df_fill.drop(['Type_de_voie', 'No_voie','Voie','Code_voie'], axis=1)
    df_fill  = df_fill.dropna(subset = ["Valeur_fonciere"] ,axis = 0)
    return df_fill

def fill_code_postal(df_fill : pd.DataFrame) -> pd.DataFrame:
    df_fill['Code_postal'] = df_fill.groupby(['Commune', 'Code_commune', 'Code_departement']).Code_postal.transform(lambda x: x.fillna(x.median()))
    return df_fill

# df_fill = Clean_df(df)
    
    #profile = ProfileReport(df_s, title="Pandas Profiling Report",html={'style':{'full_width':True}})
    #profile
    #profile_dd = ProfileReport(df_s1, title="Pandas Profiling Report",html={'style':{'full_width':True}})
    #profile_dd