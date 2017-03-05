import pandas as pd
import os

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
    df = df.drop(df.filter(axis=1, regex=('([time])')).columns, axis=1)
    _df = df['key'].str.extract('(?P<xday>\d*)(?P<county>\D*)', expand=False)                    #==> split key into date and county (?P<xday>\d*)
    df = pd.concat([df,_df],axis=1, join='outer')                   #==> add the above split to dataframe
    df.columns = df.columns.str.lower()                             #==> fix columns header issues
    df.set_index('adate')
    return df[1:]

def combine_save_csv(raw_path,csv_files):
    i = 0
    for xfile in csv_files:
        file_name = raw_path + str(xfile)
        if i > 0:
            i = i + 1
            xd = pd.read_csv(file_name)
            print len(xd), file_name
            df = pd.concat([df, xd])

        if i < 1:
            df = pd.read_csv(file_name)
            i = i + 1
            print len(df), i
    return df


if __name__ == '__main__':

    # =====================================================================
    RAW_WEATHER_FILES = '../data/darksky/'
    PROCESSED_WEATHER = '../data/counties/weather_all.csv'
    # =====================================================================

    # get all the csv files in the directory
    csv_files = [f for f in os.listdir(RAW_WEATHER_FILES) if f.endswith('.csv')]

    weather_df = combine_save_csv(RAW_WEATHER_FILES,csv_files)
    weather_df.to_csv(PROCESSED_WEATHER)