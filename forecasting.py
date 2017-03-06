import pandas as pd
import numpy as np
import scipy.stats as scs
import os
import cPickle as pickle


# ===========================================================
# ====== Key file locations =================================
# ===========================================================
COMBINED = 'data/forecast.csv'
PICKLED = 'data/pickles/reg_train_ada_ALL_xtr.pkl'


# ===========================================================
# ====== Key CONSTANTS ======================================
# ===========================================================

MIN_YEAR = 2010                 # ==> Set min year to earliest
MAX_YEAR = 2016                 # ==> Max year for full TTS data
STATE = 'CO'                   # ==> ALL is ['CO', 'MT', 'ID', 'WY']
CNTY = 'Weld'



if __name__ == '__main__':
    df = pd.read_csv(COMBINED)
    print df.head()


    state = "CO"
    irig = 1

    # xf = df.loc[df.year == yr]
    xf = df.loc[df.state == state]
    xf['irig_flag'] = 0

    ave_xf = np.mean(xf)
    # =========== Load pickle of training session ========
    with open(PICKLED) as f:
        model = pickle.load(f)

    model.predict(ave_xf)
    print model

