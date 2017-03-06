import pandas as pd
import requests
import numpy as np
import os
import cPickle as pickle

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns


from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import GridSearchCV

from src.util_download_yields import *
from src.process_weather import *


# ===========================================================
# ====== Key file locations =================================
# ===========================================================
RAW_WEATHER_FILE = 'data/weather/weather_all.csv'
# RAW_YIELD = "data/yield/yield_raw_data_all.csv"
PROCESSED_YIELD = "data/yield/yield_proc_data.csv"
COMBINED = 'data/combined.csv'
IMAGES_FOLDER = 'images/'


# ===========================================================
# ====== Key CONSTANTS ======================================
# ===========================================================

TRAIN = False                   # ==> Set mode model is in
MIN_YEAR = 2010                 # ==> Set min year to earliest
MAX_YEAR = 2017                 # ==> Max year for full TTS data
TEST_SPLIT = 2014               # ==> Sets year Train test split
STATE = 'ALL'                   # ==> ALL is ['CO', 'MT', 'ID', 'WY']

if TRAIN == False:
    MIN_YEAR = TEST_SPLIT       # ==> 2014
    MAX_YEAR = MAX_YEAR         # ==> 2016
    TEST_SPLIT = MAX_YEAR     # ==> 2016

def weather_dates(df,MIN_YEAR,MAX_YEAR):
    '''
    :param df: dataframe containing location specific weather
    :param MIN_YEAR: 2010 (start of training set)
    :param MAX_YEAR: (end of test set)
    :return:
    '''
    df['dates'] = pd.to_datetime(df['apparentTemperatureMaxTime'], unit='s')
    df['year'] = [x.year for x in df['dates']]
    df['month'] = [x.month for x in df['dates']]
    df.drop('aDate', axis = 1, inplace=True)
    df['county'] = [x.lower() for x in df['county']]

    #remove times not needed and junk columns
    df_times = df.filter(like='Time', axis=1).columns.tolist()
    df_unnamed = df.filter(like='Unnamed', axis=1).columns.tolist()
    df.drop(df_times, axis=1, inplace=True)
    df.drop(df_unnamed, axis=1, inplace=True)
    df.drop(['moonPhase', 'key', 'time', 'precipType'], axis=1, inplace=True)

    #strip out non summer growing months
    df = df.drop(df[df.month < 4].index)
    df = df.drop(df[df.month > 9].index)
    df = df.drop(df[df.year < MIN_YEAR].index)
    df = df.drop(df[df.year > MAX_YEAR].index)

    return df


def yield_dates(df,MIN_YEAR, TEST_SPLIT):

    # remove unneeded timstamps, etc
    df.dropna(axis=1, how='all', inplace=True)
    df['county_name'] = df['county_name'].apply(lambda x: x.lower())
    df.rename(columns={'county_name':'county','Value':'cyield','state_alpha':'state'}, inplace=True)
    df_unnamed = df.filter(like='Unnamed', axis=1).columns.tolist()
    df.drop('Unnamed: 0', axis=1, inplace=True)


    # drop outlier yield less than 40

    #split out years
    df = df.drop(df[df.year < MIN_YEAR].index)
    df = df.drop(df[df.year > TEST_SPLIT].index)
    return df


def join_weather_yield(wdf, ydf):
    # ========== Work magic on the weather file ==============
    wdf.drop('dates', axis=1, inplace=True)
    wdf['county'] = wdf['county'].apply(str.lower)
    DROP_LIST = ['visibility','lat', 'long','month','windBearing', 'precipProbability','aveTemp', 'pressure',
                 'windBearing','precipIntensityMax','cloudCover', 'temperatureMax', 'windSpeed',
                 'apparentTemperatureMax']

    # ======== add new features here =========================
    wdf['aveTemp'] = (wdf['temperatureMax'] + wdf['temperatureMin'])/2
    wdf['temp_delta'] = (wdf['temperatureMax'] - wdf['temperatureMin'])
    wdf['days_over42'] = wdf['temperatureMax'].map(lambda x: is_over(x, 42))
    wdf['days_under0'] = wdf['temperatureMin'].map(lambda x: is_under(x, -20))
    wdf['days_over32'] = wdf['temperatureMax'].map(lambda x: is_over(x, 32))
    wdf['days_under_n10'] = wdf['temperatureMin'].map(lambda x: is_under(x, -10))
    wdf['precip'] = wdf['precipIntensity'].map(lambda x: is_over(x, 0.0))

    # === test see if i need to narrow the weather window to average
    # wdf = wdf.drop(wdf[wdf.month < 4].index)
    # wdf = wdf.drop(wdf[wdf.month > 9].index)
    wdf.drop(DROP_LIST, axis=1, inplace=True)



    # ======= prepare column list for sum and mean aggregations by state, county, year
    agg_dict = dict()
    cols_list = list(wdf.columns.tolist())
    group_by_columns = ['county','state','year']
    cols_to_sum = ['days_under0', 'days_over32', 'days_over42' , 'days_under_n10', 'precipAccumulation', 'precip']
    cols_to_aggregate = [x for x in cols_list if x not in group_by_columns]
    for i in cols_to_aggregate:
        if i in cols_to_sum:
            agg_dict[i]= np.sum
        else:
            agg_dict[i] = np.mean

    print "Fixing resulting NAs and missing data"
    wdf_years = wdf.groupby(group_by_columns).agg(agg_dict)

    # fix nans in precip accumulation for days of no accumulation
    wdf_years['precipAccumulation'].fillna(0, inplace=True)

    # save the processed weather file for later use
    wdf_years.to_csv(PROC_WEATHER_FILE)
    wdf_years = pd.read_csv(PROC_WEATHER_FILE)

    # ========== Work magic on the yield file ==============
    ydf.groupby(group_by_columns).mean()
    df_merged = pd.merge(ydf,wdf_years, how='left',on=['county','state','year'])
    df_merged.dropna(axis=0,how='any',inplace=True)
    return df_merged


def is_over(x,val):
    '''
    simple helper function for counting...
    :param x: value of data point
    :param val: comparision value
    :return: returns a value 1 if it is greater than val 0 if lower
    '''
    if x>val: return 1
    else: return 0

def is_under(x,val):
    '''
    simple helper function for counting...
    :param x: value of data point
    :param val: comparision value
    :return: returns a value 0 if it is greater than val 1 if lower
    '''
    if x<val: return 1
    else: return 0


def my_ada(X,y,m_depth=3,n_est=28,rnd=None,lr=0.8225):
    '''
    quick wrapping function for sklearn ada_boost analysis
    :param X:
    :param y:
    :param m_depth: max depth of Dtree 'stumps'
    :param n_est: number of estimators to use
    :param rnd: sets the random seed if you want
    :param lr: learning rate
    :return: returns the model fully fitted and predicted
    '''
    reg_ada = AdaBoostRegressor(DecisionTreeRegressor(max_depth=m_depth),\
                                n_estimators=n_est,random_state=rnd, learning_rate=lr)
    reg_ada.fit(X,y)
    reg_ada.predict(X)
    return reg_ada


def feature_importance(cols,feat_imps):
    '''
    function to assign feature names to feature importance list out of sklearn
    :param cols: is the pands data series containing the list of features
    :param feat_imps: the data series containing the resulting feature importance values
    :return: returns a consolidated pandas DF of the features and there determined importance
    '''
    df = pd.DataFrame()
    df['feat'] = cols
    df['imp'] = feat_imps
    df.sort_values('imp',ascending=False, inplace=True)
    df = df.loc[df['imp'] > 0]
    df.reset_index()
    df.drop('index')
    return df



if __name__ == '__main__':

    print 'Loading raw weather data....'
    df_weather  = weather_dates(pd.read_csv(RAW_WEATHER_FILE),MIN_YEAR,TEST_SPLIT)

    print 'Loading yield files.........'
    df_yield = yield_dates(pd.read_csv(PROCESSED_YIELD),MIN_YEAR,TEST_SPLIT)

    print 'combining the two files for analysis'
    df_join = join_weather_yield(df_weather, df_yield)
    df_join.to_csv(COMBINED)

    # Code block for fine tuning and EDA experimentation
    # ==============================================
    _dummy = df_join[df_join['cyield'] >= 50]
    _dummy = df_join[df_join['cyield'] <= 180]
    if not STATE == 'ALL': _dummy = df_join[df_join.state != 'ID']
    sfl = _dummy
    _dummy.pop('year')
    _dummy.pop('county')
    _dummy = pd.get_dummies((_dummy))
    # ==============================================


    # Preping the y and X variables for input to Adaboost
    # ==============================================
    y = _dummy.pop('cyield')
    X = _dummy

    # RUN ADABOOST  lr=0.862, n_est=5
    # =============================================
    print '\n\n'
    print 'Running model on TRAIN? ', TRAIN
    if TRAIN == False:
        # =========== Load pickle of training session ========
        with open('data/pickles/reg_ada_'+STATE+'_xtr.pkl') as f:
            reg_ada = pickle.load(f)
    else:
        # ===========  Run Adaboost fit-pred  ================
        reg_ada = my_ada(X, y, m_depth=3, n_est=8, rnd=42, lr=1.28225)

        # ===========  Do GRIDSEARCH analysis ================
        lr_range = np.linspace(0.1,10,100)
        n_est = [int(i) for i in (np.linspace(5,100,1))]
        params = {'n_estimators' : n_est, 'learning_rate':lr_range}
        grid = GridSearchCV(estimator=reg_ada, param_grid=params,n_jobs=-1, return_train_score=True)
        grid.fit(X,y)
        _best_params =  grid.best_params_

    # predict and score
    y_ada = reg_ada.predict(X)
    ada_mse = mse(y, y_ada)
    print '\n\n'
    print 'TRAINING SET? ',TRAIN
    print 'STATES: %s  Dates: %s --> %s' %(STATE,MIN_YEAR,TEST_SPLIT)
    print '================================================'
    print 'Adaboost   r2:   ', reg_ada.score(X,y)
    print 'Adaboost  MSE:   ', ada_mse
    print 'Adaboost RMSE:   ', np.sqrt(ada_mse)
    print '================================================'
    # print 'Used : ', reg_ada.get_params()

    # Extract table of most important features for later use if needed
    feat_imp = feature_importance(X.columns.tolist(),reg_ada.feature_importances_)
    # print feat_imp

    # =========== Save pickle of training session ===========
    if TRAIN == True:
        with open('data/pickles/reg_train_ada_'+STATE+'_xtr.pkl', 'wb') as f:
            pickle.dump(reg_ada, f)

    # =========== Plot overall y_true and y_predicted ===========
    res = sfl
    res['y_pred']=y_ada
    res.to_csv('data/forecast.csv', index=False)
    df_plt = res
    df_plt['y_true'] = y

    plt.close('all')
    # fig = plt.figure()
    sns.regplot(x='y_true',y='y_pred',data=df_plt, label='state', marker='o', scatter_kws={'s':80});
    plt.title(STATE + ' regression performance', fontsize=30);
    plt.xlabel('y_true (bu/acre)')
    plt.ylabel('y_pred (bu/acre)')
    plt.legend()
    plt.savefig(IMAGES_FOLDER + 'model_yt_yp.jpg')
    plt.show()


    # # =========== Plot by State y_true and y_predicted ===========
    # g = sns.FacetGrid(res, col='irig_flag', hue='state')
    # g.map(sns.regplot, 'y_true', 'y_pred', label='state', marker='o', scatter_kws={'s':80});
    # plt.xlim(0, 180)
    # plt.ylim(0, 180)
    # plt.legend()
    # plt.show()
    #
    # # =========== Plot by IRIG_FLAG y_true and y_predicted ===========
    # g = sns.FacetGrid(res, col='state', hue='irig_flag')
    # g.map(sns.regplot, 'y_true', 'y_pred', label='state', marker='o', scatter_kws={'s':80});
    # plt.xlim(0, 180)
    # plt.ylim(0, 180)
    # plt.legend()
    # plt.show()


    fig = plt.subplot(211)
    plt.plot(res.y_true, marker='o', lw=0)
    plt.plot(res.y_pred, lw=2)
    # plt.title(STATE + ' regression performance', fontsize=25);
    plt.xlabel('data-point')
    plt.ylabel('yield (bu/acre)')
    plt.ylim([0, 180])
    plt.title('Model Performance',fontsize=30)
    plt.savefig(IMAGES_FOLDER + 'model_performance_test.jpg')
    plt.show()

