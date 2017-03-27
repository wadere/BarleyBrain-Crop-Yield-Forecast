import pandas as pd
import os
import glob

# CHECKED AND GOOD 2/26/2016

def make_unixdate(xdate):
    # takes a timestamp and coverts it to unix time
    myts = int(time.mktime(xdate.timetuple()))
    return myts


def clean_data(df):
    '''
    function for cleaning the data extracted directly from
    darkskynet saves  done in funtion darksky_hist_weather.py
    '''
    # df = df.drop(df.filter(axis=1, regex=('([Unamed])')).columns, axis=1)
    time_cols = df.filter(axis=1, regex=('([time])')).columns.tolist()
    df.columns = df.columns.str.lower()                             #==> fix columns header issues
    df.county = df.county.str.lower()
    df.drop_duplicates(inplace=True)
    return df[1:]

def combine_csv(raw_path):
    # i = 0
    # for xfile in csv_files:
    #     file_name = raw_path + str(xfile)
    #     if i > 0:
    #         i = i + 1
    #         xd = pd.read_csv(file_name)
    #         print len(xd), file_name
    #         df = pd.concat([df, xd])
    #
    #     if i < 1:
    #         df = pd.read_csv(file_name)
    #         i = i + 1
    #         print len(df), i

    df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(raw_path, "*.csv"))))
    df.avetemp = 0.5*df.temperatureMax + 0.5*df.temperatureMin
    df=clean_data(df)
    try:
        df.drop('unnamed: 0',inplace=True, axis=1)
        # df.drop('key', inplace=True, axis=1)
        df.drop('Unnamed: 0', inplace=True, axis=1)
    except:
        pass

    # df.drop_duplicates(inplace=True)
    return df[1:]


if __name__ == '__main__':

    # =====================================================================
    RAW_WEATHER_FILES = 'data/darksky/'
    PROCESSED_WEATHER = 'data/counties/weather_all_nd_pi5.csv'
    # =====================================================================

    # # get all the csv files in the directory
    # csv_files = [f for f in os.listdir(RAW_WEATHER_FILES) if f.endswith('.csv')]

    weather_df = combine_csv(RAW_WEATHER_FILES)
    weather_df.to_csv(PROCESSED_WEATHER, index=False)