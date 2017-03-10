import requests
import time
import os
from datetime import date
import pandas as pd


# CHECKED AND GOOD 2/26/2016


def get_weather(api_key, lat, lng, ste, cnty, mydate):
    utcday = make_unixdate(mydate)
    tmreq = 'https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]?exclude=currently,flags,hourly'
    weather_url = tmreq.replace('[key]', api_key).replace('[longitude]', str(round(lng, 10))) \
        .replace('[latitude]', str(round(lat, 10))).replace('[time]', str(utcday))
    w_data = requests.get(weather_url).json()
    w_data = w_data['daily']['data'][0]

    #     w_data = requests.get(weather_url).json()['daily']['data'][0]

    # strip out commenting text,text
    w_data.pop('summary', None)
    w_data.pop('icon', None)
    w_data.pop('year.1',None)
    df = pd.DataFrame.from_dict(w_data, orient='index').transpose()
    df['avetemp'] = (df['temperatureMax'] + df['temperatureMax'])/2.0
    # df['key'] = str(utcday) + '_' + str(cnty)
    # df['aDate'] = mydate
    df['county'] = cnty
    df['state'] = ste
    return df


def make_unixdate(xdate):
    # takes a timestamp and coverts it to unix time
#     print xdate.timetuple()
    myts = int(time.mktime(xdate.timetuple()))
    return myts




if __name__ == '__main__':
    API_KEY = ""
    lat = 37.8267
    lon = -122.4233
    county = 'WELD'
    state = 'CO'
    COUNTY_LATS= 'data/counties/county_lat_lng.csv'

    S_YEAR = 2009
    S_MONTH = 04
    S_DAY = 01
    E_YEAR = 2009
    E_MONTH = 10
    E_DAY = 01
    start_time = date(S_YEAR, S_MONTH, S_DAY)
    end_time = date(E_YEAR, E_MONTH, E_DAY)
    myts = int(time.mktime(start_time.timetuple()))

    # setup daterange for datapulls
    mydates = pd.date_range(start_time, end_time, freq='D').tolist()

    # jj=  os.getcwd()
    county_df = pd.read_csv(COUNTY_LATS)
    weather_df = get_weather(API_KEY,lat,lon,state,county,start_time)
    full_df = weather_df
    

    # =========== Pull all data by county, then by date ==========================
    for item in range(1,len(county_df)):   #==> len(county_df) 187
        full_df = weather_df
        state = county_df['USPS'][item]
        county = county_df['NAME'][item]
        lon = county_df['LONG'][item]
        lat = county_df['LAT'][item]

        for xd in mydates:
            utcday = make_unixdate(xd)
            print xd, utcday, state, county, round(lat, 4), round(lon, 4)
            day_df = pd.DataFrame(get_weather(API_KEY, lat, lon, state, county, xd))
            full_df = full_df.append(day_df)

        # save completed county data
        f_name = str(S_YEAR) + '-' + str(E_YEAR) + '__' + state + '_' + county + '.csv'
        print f_name
        full_df.to_csv(f_name)