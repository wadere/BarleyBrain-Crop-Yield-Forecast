import cPickle as pickle
import numpy as np
import pandas as pd

# ===========================================================
# ====== Key file locations =================================
# ===========================================================
COMBINED = 'data/forecast.csv'
PICKLED = 'data/pickles/reg_train_ada_ALL_xtr.pkl'

if __name__ == '__main__':
    '''
    This script runs in conjunction with BarleyBrain.py and the web_app at Barley_Brain.com
    before running make sure that the 'pre processed' forecast file as above.
    Also, make sure you have run BarleyBrain.py in train and test mode to establish the pickle for
    online prediction and modeling.
    '''

    #  List of columns the pickled model is expecting
    cols = ['irig_flag',
            'days_under0',
            'dewPoint',
            'precipAccumulation',
            'precip',
            'days_under_n10',
            'days_over42',
            'days_over32',
            'temp_delta',
            'temperatureMin',
            'apparentTemperatureMin',
            'precipIntensity',
            'asd_desc_CENTRAL',
            'asd_desc_EAST',
            'asd_desc_NORTH',
            'asd_desc_NORTH CENTRAL',
            'asd_desc_NORTHEAST',
            'asd_desc_NORTHWEST',
            'asd_desc_SAN LUIS VALLEY',
            'asd_desc_SOUTH CENTRAL',
            'asd_desc_SOUTHEAST',
            'asd_desc_SOUTHWEST',
            'state_CO',
            'state_ID',
            'state_MT',
            'state_WY']

    # load the pre processed file
    df = pd.read_csv(COMBINED)

    # drop the columns that have y_pred, and cyield in them and
    # then do get_dummies to get the df in proper form for model
    df.drop(['y_pred', 'cyield'], axis=1, inplace=True)
    df = pd.get_dummies(df, drop_first=False)

    # manual set of region and state for testing replace with web app calls
    region = 'SAN LUIS VALLEY'
    state = "CO"

    # filter pre-processed data to only the region indicated from above
    xcol = 'asd_desc_' + region
    # noinspection PyUnresolvedReferences
    xf = df.loc[df[xcol] == 1.0]

    # now, compress the last 3 years of weather data down to an average for prediction
    ave_xf = np.mean(xf)

    # =========== Load pickle of training session ========
    with open(PICKLED) as f:
        model = pickle.load(f)
    y = model.predict(ave_xf.reshape(1, -1))

    print 'Your forecast for this season in:'
    print '%s portion of %s is:' % (region, state,)
    print "Prediction is %s bushels/acre" % y
    print '\n\n'
