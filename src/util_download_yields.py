import pandas as pd
import requests
import numpy as np
import os

import statsmodels.api as sm
import scipy.stats as stats

# from matplotlib import pyplot as plt
# import seaborn as sns


def get_gov_yield(syear=2005, eyear=2020, state='CO'):
    # Make API call
    url = "http://quickstats.nass.usda.gov/api/api_GET/?" + \
          "key={}&".format(os.environ["NASS_API_KEY"]) + \
          "commodity_desc=BARLEY&" + \
          "group_desc=FIELD CROPS&" + \
          "sector_desc=CROPS&" + \
          "source_desc=SURVEY&" + \
          "statisticcat_desc=YIELD&" + \
          "short_desc__NOT_LIKE=SILAGE&" + \
          "year__GE=" + str(syear) + "&" + \
          "year__LE=" + str(eyear) + "&" + \
          "format=json"
    #          "state_alpha=" + state + "&" + \

    print 'Downloading data now.......'
    response = requests.get(url)
    print response

    # Create DataFrame
    data = response.json()
    df = pd.DataFrame(data['data'])

    # # Clean the data
    df["cyield"] = df.Value.map(float)
    df["year"] = df.year.map(int)
    df.drop_duplicates()
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)

    df = df.loc[df['agg_level_desc'] == 'COUNTY']
    df = df.loc[df['reference_period_desc'] == 'YEAR']
    dropme = ['class_desc', 'agg_level_desc', 'congr_district_code', 'country_code', 'state_fips_code',
              'watershed_code','watershed_desc', 'week_ending', 'zip_5', 'begin_code', 'country_name',
              'county_ansi', 'county_code','state_ansi', 'sector_desc', 'domain_desc', 'end_code', 'CV (%)',
              'freq_desc', 'group_desc','domaincat_desc','load_time', 'prodn_practice_desc', 'region_desc', 'source_desc', 'util_practice_desc', 'commodity_desc', \
              'statisticcat_desc', 'asd_code', 'location_desc']

    # drop county data not specifically named (aka OTHER or blank)
    df.drop(dropme, axis=1, inplace=True)
    df['county_name'].dropna(axis=0, how='any', inplace=True)
    df.drop(['reference_period_desc', 'short_desc', 'state_name', 'unit_desc', 'Value'], axis=1, inplace=True)
    df = df.loc[df['year'] <= eyear]
    df = df.loc[(df['state_alpha'] == 'MT')|(df['state_alpha'] == 'CO')|(df['state_alpha'] == 'WY')|(df['state_alpha'] == 'ID')]
    # df = df.loc[(df['state_alpha'] == state)]
    # df.drop(df[df.county_name == 'OTHER (COMBINED) COUNTIES'].index, inplace=True)
    df['irig_flag'] = np.where(df['cyield'] >= 75, 1, 0)
    return df

if __name__ == '__main__':

    MIN_YEAR = 2010
    MAX_YEAR = 2020
    # YIELD_FILE = '../data/yield/yield_raw_data_state.csv'
    PROCESSED_YIELD_FILE = "../data/yield/yield_proc_data.csv"

    df = get_gov_yield(MIN_YEAR,MAX_YEAR,None)
    print 'Saving file'
    print df.head()
    df.to_csv(PROCESSED_YIELD_FILE)
