import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
from math import sqrt

import datetime as dt

def generate_area(file,
                  sep,
                  group = False):
    df = pd.read_csv(file, sep=sep)

    # Set Horodate column to current year
    df['Horodate'] = pd.to_datetime('2025.' + df['Horodate'], format='%Y.%d.%m. %H:%M')

    # Replace ',' by '.' for all columns except first one which is Horodate
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(',','.').astype(float)

    # Group by type of consumers
    if group:
        df['Parking_Harmony'] = df['Parking_Harmony1\nauto_cons'] \
                                + df['Parking_Harmony2\nauto_cons']
        df.drop(['Parking_Harmony1\nauto_cons','Parking_Harmony2\nauto_cons'],
                axis=1, inplace=True)

        df['ParvisDuBreuil'] = df['1ParvisDuBreuil\nauto_cons'] \
                                + df['2ParvisDuBreuil\nauto_cons'] \
                                + df['3ParvisDuBreuil\nauto_cons']
        df.drop(['1ParvisDuBreuil\nauto_cons','2ParvisDuBreuil\nauto_cons','3ParvisDuBreuil\nauto_cons'],
                axis=1, inplace=True)

        df['ParvisDeLaBievre'] = df['2ParvisDeLaBievre\nauto_cons'] \
                                + df['3ParvisDeLaBievre\nauto_cons'] \
                                + df['5ParvisDeLaBievre\nauto_cons']
        df.drop(['2ParvisDeLaBievre\nauto_cons','3ParvisDeLaBievre\nauto_cons','5ParvisDeLaBievre\nauto_cons'],
                axis=1, inplace=True)

    # Add last column with contain difference between production and all auto_consumption
    df['Remaining_prod'] = df.iloc[:,1] - df.iloc[:,2:-1].sum(axis=1)
    df.drop(['auto_cons_rate'],axis=1, inplace=True)

    print('df: ',df.head())

    # Add auto_cons value on the same column and add another column for cons id
    list_df = list()
    area = pd.DataFrame()
    for index, col in enumerate(df.columns[2:]):
        list_df.append(pd.DataFrame())

        list_df[index]['Horodate'] = df['Horodate']
        list_df[index]['auto_cons'] = df[col]
        list_df[index]['id_cons'] = df.columns[index+2].replace('\nauto_cons','')
        area = pd.concat([area,list_df[index]])
        # print(list_df[index].head())

    area['Month'] = area['Horodate'].dt.month_name()

    # Select only data for each hour to reduce data
    area_hours = area[area['Horodate'].dt.minute == 0]
    area_hours.reset_index(drop=True, inplace=True)

    print('area_hours: ',area_hours.tail())

    # fig = px.area(area_hours,
    #               x='Horodate',
    #               y='auto_cons',
    #               color='id_cons',
    #               title='Profil d\'autoconsommation des consommateurs',
    #               labels={'Horodate': 'Date', 'auto_cons': 'Autoconsommation (Wh)'},
    #               animation_frame='Month')

    # Get day and month values
    area['day'] = area['Horodate'].dt.day
    area['month'] = area['Horodate'].dt.month

    # Create pivot table to summarize consumption
    piv = pd.pivot_table(area, values='auto_cons', index=['id_cons', 'month', 'day'], aggfunc='sum')
    piv.reset_index(inplace=True)
    piv['month'] = piv['month'].astype(str)
    piv['day'] = piv['day'].astype(str)
    piv['date'] = pd.to_datetime('2025.' + piv['month'] + '.' + piv['day'], format='%Y.%m.%d')

    fig = px.area(piv,
                  x='date',
                  y='auto_cons',
                  color='id_cons',
                  title='Profil d\'autoconsommation par consommateur',
                  labels={'Horodate': 'Date', 'auto_cons': 'Autoconsommation (kWh)'})

    # fig = px.histogram(df,
    #                    x='Horodate',
    #                    y='Prod1',
    #                    title='Production et auto_consommation',
    #                    nbins=12)

    # fig = px.line(df,
    #               x='Horodate',
    #               y='Parking_Harmony1\nauto_cons',
    #               title='Production',
    #               markers=True,  # Ajoute des marqueurs aux points de données
    #               line_shape='linear')  # Ligne continue entre les points
    #
    # fig = px.histogram(df,
    #                    x='Horodate',
    #                    y='Prod1',
    #                    title='Production et auto_consommation',
    #                    nbins=12)

    fig.show()


def generate_month_graph(file, sep):
    df = pd.read_csv(file, sep=sep)

    # Set Horodate column to current year
    df['Horodate'] = pd.to_datetime('2025.' + df['Horodate'], format='%Y.%d.%m. %H:%M')

    # Replace ',' by '.' for all columns except first one which is Horodate
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    df['Parking_Harmony'] = df['Parking_Harmony1\nauto_cons_mois'] \
                            + df['Parking_Harmony2\nauto_cons_mois']
    df.drop(['Parking_Harmony1\nauto_cons_mois','Parking_Harmony2\nauto_cons_mois'],
            axis=1, inplace=True)

    df['ParvisDuBreuil'] = df['1ParvisDuBreuil\nauto_cons_mois'] \
                            + df['2ParvisDuBreuil\nauto_cons_mois'] \
                            + df['3ParvisDuBreuil\nauto_cons_mois']
    df.drop(['1ParvisDuBreuil\nauto_cons_mois','2ParvisDuBreuil\nauto_cons_mois','3ParvisDuBreuil\nauto_cons_mois'],
            axis=1, inplace=True)

    df['ParvisDeLaBievre'] = df['2ParvisDeLaBievre\nauto_cons_mois'] \
                            + df['3ParvisDeLaBievre\nauto_cons_mois'] \
                            + df['5ParvisDeLaBievre\nauto_cons_mois']
    df.drop(['2ParvisDeLaBievre\nauto_cons_mois','3ParvisDeLaBievre\nauto_cons_mois','5ParvisDeLaBievre\nauto_cons_mois'],
            axis=1, inplace=True)

    # Add last column with contain difference between production and all auto_consumption
    df['Remaining_prod'] = df.iloc[:,1] - df.iloc[:,2:].sum(axis=1)

    print('df: ',df.head())

    # Add auto_cons value on the same column and add another column for cons id
    list_df = list()
    area = pd.DataFrame()
    for index, col in enumerate(df.columns[2:]):
        # area = pd.DataFrame()
        list_df.append(pd.DataFrame())

        list_df[index]['Horodate'] = df['Horodate']
        list_df[index]['auto_cons_mois'] = df[col]
        list_df[index]['id_cons'] = df.columns[index + 2].replace('\nauto_cons_mois', '')
        area = pd.concat([area, list_df[index]])
        # print(list_df[index].head())

    print('area: ',area.head())

    fig = px.area(area,
                  x='Horodate',
                  y='auto_cons_mois',
                  color='id_cons',
                  title='Profil d\'autoconsommation par consommateur',
                  labels={'Horodate': 'Date', 'auto_cons': 'Autoconsommation (Wh)'})

    # fig = px.histogram(df,
    #                    x='Horodate',
    #                    y='Prod1',
    #                    title='Production et auto_consommation',
    #                    nbins=12)

    # fig = px.line(df,
    #               x='Horodate',
    #               y='Parking_Harmony1\nauto_cons',
    #               title='Production',
    #               markers=True,  # Ajoute des marqueurs aux points de données
    #               line_shape='linear')  # Ligne continue entre les points
    #
    # fig = px.histogram(df,
    #                    x='Horodate',
    #                    y='Prod1',
    #                    title='Production et auto_consommation',
    #                    nbins=12)

    fig.show()

