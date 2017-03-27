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
    API_KEY = "b96da89533e3d3e1f40f560603a30fee"
    lat = 37.8267
    lon = -122.4233
    county = 'WELD'
    state = 'CO'
    COUNTY_LATS= 'data/counties/county_lat_lng.csv'

    S_YEAR = 2017
    S_MONTH = 04
    S_DAY = 01
    E_YEAR = 2017
    E_MONTH = 10
    E_DAY = 01
    start_time = date(S_YEAR, S_MONTH, S_DAY)
    end_time = date(E_YEAR, E_MONTH, E_DAY)
    myts = int(time.mktime(start_time.timetuple()))

    # setup daterange for datapulls
    mydates = pd.DataFrame(pd.date_range(start_time, end_time, freq='D').tolist())
    mydates['dates'] = mydates[0]
    mydates['month'] = [i.month for i in mydates['dates']]
    mydates = mydates.drop(mydates[mydates.month >= E_MONTH].index)
    mydates = mydates.drop(mydates[mydates.month < S_MONTH].index)

    # jj=  os.getcwd()
    county_df = pd.read_csv(COUNTY_LATS)
    weather_df = get_weather(API_KEY, lat, lon, state, county, start_time)
    full_df = weather_df

    # =========== Pull all data by county, then by date ==========================
    for item in range(1, len(county_df)):  # ==> len(county_df) 187
        full_df = weather_df
        state = county_df['USPS'][item]
        county = county_df['NAME'][item]
        lon = county_df['LONG'][item]
        lat = county_df['LAT'][item]
        f_name = 'data/darksky/' + str(S_YEAR) + '-' + str(E_YEAR) + '__' + state + '_' + county + '.csv'

        # pool = ThreadPool(4)
        # results = pool.map(get_weather(API_KEY,lat,lon,state,county,xd),mydates)
        #
        print  '%s of %s....checking if record exists for : %s' % (item, len(county_df), f_name)
        if not os.path.exists(f_name):
            if state != "XX":
                for xd in mydates.dates:
                    # utcday = make_unixdate(xd)
                    print item, xd, state, county, round(lat, 4), round(lon, 4)
                    day_df = pd.DataFrame(get_weather(API_KEY, lat, lon, state, county, xd))
                    full_df = full_df.append(day_df)

                # save completed county data
                print item, ' ', f_name
                full_df.drop_duplicates(keep='first', inplace=True)
                full_df.to_csv(f_name, index=False)