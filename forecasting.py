import pandas as pd
import numpy as np
import scipy.stats as scs
import os
import cPickle as pickle


# ===========================================================
# ====== Key file locations =================================
# ===========================================================
RAW_WEATHER_FILE = 'data/weather/weather_all.csv'
# RAW_YIELD = "data/yield/yield_raw_data_all.csv"
PROCESSED_YIELD = "data/yield/yield_proc_data.csv"
COMBINED = 'data/combined.csv'
IMAGES_FOLDER = 'images/'
PICKLED = 'data/pickles/reg_train_ada_ALL_xtr.pkl'


# ===========================================================
# ====== Key CONSTANTS ======================================
# ===========================================================

TRAIN = True                   # ==> Set mode model is in
MIN_YEAR = 2010                 # ==> Set min year to earliest
MAX_YEAR = 2016                 # ==> Max year for full TTS data
TEST_SPLIT = 2014               # ==> Sets year Train test split
STATE = 'ALL'                   # ==> ALL is ['CO', 'MT', 'ID', 'WY']




if __name__ == '__main__':
    df = pd.read_csv(COMBINED)
    print df.head()

    yr = yr = 2013
    state = "CO"
    irig = 1

    xf = df.loc[df.year == yr]
    xf = xf.loc[xf.state == state]
    xf['irig_flag'] = 0

    # =========== Load pickle of training session ========
    with open(PICKLED) as f:
        model = pickle.load(f)

    print model

