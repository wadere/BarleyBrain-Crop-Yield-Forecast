import pandas as pd
import numpy as np
import os
from datetime import datetime

# from matplotlib import pyplot as plt
# import seaborn as sns



MIN_YEAR = 2010
MAX_YEAR = 2020
RAW_WEATHER_FILE = 'data/weather/weather_all.csv'
PROC_WEATHER_FILE = 'data/weather/weather_clean.csv'

# =====================================================================

def load_files(file_name):
    df = pd.read_csv(file_name)
    # clean up "all nans
    df.dropna(axis=0,how='all',inplace=True)
    # df.dropna(axis=1,how='all',inplace=True)
    return df

def weather_clean(df,syear,eyear):
    # fix times and drop un-needed stuff
    print 'Formating dates, and time columns'

    df['dropme'] = pd.to_numeric([('20' + (x.split(' ')[0]).split('/')[2])*1 for x in df['aDate']])
    df = df.loc[df['dropme'] >= MIN_YEAR]

    # df['year_day'] = pd.to_datetime(df['aDate'])
    df['year_month'] = pd.to_numeric([('20' + (x.split(' ')[0]).split('/')[0])*1 for x in df['aDate']])
    df['year'] = df['dropme']
    df.drop('dropme', axis=1)

    print 'Filter out columns not needed'
    df_times = df.filter(like='Time',axis=1).columns.tolist()
    df_unnamed = df.filter(like='Unnamed',axis=1).columns.tolist()

    # removing columns not needed
    df.drop(df_times,axis=1,inplace=True)
    df.drop(df_unnamed,axis=1,inplace=True)
    df.drop(['aDate','moonPhase','key','time','precipType'],axis=1,inplace=True)
    # strip out non summer growing months (10,11,12,1,2,3)
    df = df.drop(df[df.year_month < 4].index)
    df = df.drop(df[df.year_month > 9].index)
    df = df.drop(df[df.year < syear].index)
    df = df.drop(df[df.year > eyear].index)


    print 'building table and fixing NANs'
    # Taking care of the nans as first pass analysis
    df['precipAccumulation'].astype(float)
    df['cloudCover'].fillna(method='bfill',inplace=True)                 # ===> assume missing cloud data....had no clouds
    df['pressure'].fillna(method='pad',inplace=True)        # ===> assume pressure is ~ same as previous day
    df['precipIntensity'].fillna(0,inplace=True)                 # ===> assume if missing data....had no rain.no intens
    df['precipIntensityMax'].fillna(0,inplace=True)                 # ===> assume if missing data....had no rain.no intens
    df['avetemp']= (df.temperatureMax  + df.temperatureMin) /2
    df['precipAccumulation'].fillna('0',inplace=True)        # ===> assume preciAccum is ~ same as previous day
    df['precipAccumulation'] = df['precipAccumulation'].apply(lambda x: float(x))

    # =========== add a couple of features to the data  ==================
    df['days_over42'] = df['temperatureMax'].map(lambda x: is_over(x,52))
    df['days_under0'] = df['temperatureMin'].map(lambda x: is_under(x,0))
    df['days_over32'] = df['temperatureMax'].map(lambda x: is_over(x,32))
    df['days_under_n10'] = df['temperatureMin'].map(lambda x: is_under(x,-5))

    # group the columns by year and get means/sum of specific columns for analysis
    cols_to_aver = ['apparentTemperatureMax', 'apparentTemperatureMin', 'cloudCover', 'dewPoint', 'humidity', 'lat',
                    'long', 'precipIntensity', 'precipIntensityMax', 'precipProbability',
                    'pressure', 'temperatureMax', 'temperatureMin', 'visibility', 'windBearing', 'windSpeed',
                    'year_month', 'year', 'avetemp']

    cols_to_sum = ['days_under0', 'days_over42', 'days_under_n10', 'precipAccumulation']

    # groupby_columns = df['county'],df['year']
    # df_years  = df.groupby(groupby_columns).mean()
    # cols_to_sum = ['days_under0', 'days_over42','days_over40','days_under_n10','precipAccumulation']
    # df_years_sum = df.groupby(groupby_columns).sum()
    # df_years[cols_to_sum] = df_years_sum[groupby_columns]
    df_years = df.groupby(['county', 'year']).agg({'days_under0': np.sum,
                                                     'days_over32': np.sum,
                                                     'days_under_n10': np.sum,
                                                     'precipAccumulation': np.sum,
                                                     'days_over42': np.sum,
                                                     'days_over32': np.sum,
                                                     'temperatureMax': np.mean,
                                                     'temperatureMin': np.mean,
                                                     'apparentTemperatureMin': np.mean,
                                                     'cloudCover': np.mean,
                                                     'dewPoint': np.mean,
                                                     'humidity': np.mean,
                                                     'lat': np.mean,
                                                     'long': np.mean,
                                                     'precipIntensity': np.mean,
                                                     'precipIntensityMax': np.mean,
                                                     'precipProbability': np.mean,
                                                     'pressure': np.mean,
                                                     'visibility': np.mean,
                                                     'windBearing': np.mean,
                                                     'windSpeed': np.mean,
                                                     'year_month': np.mean,
                                                     'year': np.mean,
                                                     'avetemp': np.mean })
    # save out the file for later combining with yield data
    print 'Saving processed weather file to..:', PROC_WEATHER_FILE
    df_years['precipAccumulation'].fillna(0,inplace=True)
    df_years.to_csv(PROC_WEATHER_FILE)
    df = pd.read_csv(PROC_WEATHER_FILE)
    return df

def is_over(x,val):
    if x>val: return 1
    else: return 0

def is_under(x,val):
    if x<val: return 1
    else: return 0


if __name__ == '__main__':

    # print os.getcwd()
    ''' routines for combining all the raw weather file information '''
    df = load_files(RAW_WEATHER_FILE)
    df = weather_clean(df,MIN_YEAR,MAX_YEAR)

    # # save out the file for later combining with yield data
    print 'Saving cleaned weather file to..:', PROC_WEATHER_FILE
    df.to_csv(PROC_WEATHER_FILE)