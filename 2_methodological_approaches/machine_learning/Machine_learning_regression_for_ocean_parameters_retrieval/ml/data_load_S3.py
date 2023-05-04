__author__ = 'Gonzalo Mateo-García, Ana Ruescas'

import pandas as pd
from sklearn.model_selection import train_test_split
import os

PATH_TO_DATA_TRAIN_C2X = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "C2_train.txt")
PATH_TO_DATA_TEST_C2X = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "C2_test.txt")
PATH_TO_MODELS_C2X = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

bands_S3_C2X = ['400', '412.5', '442.5', '490', '510', '560',
                '620', '665','673.75','681.25', '708.75','753.75',
                '778.75','865',
                '885']

#bands_S3ratio = ['S3ratio1','S3ratio2']

#bands_S3_plus_ratios_C2X = bands_S3_C2X + bands_S3ratio

bands_try_C2X=dict([("S3bands", bands_S3_C2X)
                #('S3ratio1',['S3ratio1']),
                #('S3ratio2',['S3ratio2']),
                #('S3bands&ratios', bands_S3_plus_ratios_C2X),
                #("ratios_S3",bands_S3ratio)
                   ])

#ALL_BANDS_C2X = bands_S3_plus_ratios_C2X
ALL_BANDS_C2X = bands_S3_C2X
CDOM_C2X_variable_name = 'a_440_cdom'
TSM_C2X_variable_name = 'TSM'
CHL_C2X_variable_name = 'Chl'
TARGET_VARIABLES_C2X = [CDOM_C2X_variable_name,TSM_C2X_variable_name,CHL_C2X_variable_name]
TARGET_VARIABLES_C2X_NAMED = dict(zip(["CDOM","TSM","Chl"],TARGET_VARIABLES_C2X))


def load_C2X(path_to_train=PATH_TO_DATA_TRAIN_C2X,
             path_to_test=PATH_TO_DATA_TEST_C2X,
             target_variables=CHL_C2X_variable_name):

    skdata = pd.read_csv(path_to_train, sep='\t', na_values=' ')

    #skdata['S3ratio1'] = skdata['665'] / skdata['490']
    #skdata['S3ratio2'] = skdata['708.75'] / skdata['490']


    skdata_test = pd.read_csv(path_to_test,
                              sep='\t', na_values=' ')

    #skdata_test['S3ratio1'] = skdata_test['665'] / skdata_test['490']
    #skdata_test['S3ratio2'] = skdata_test['708.75'] / skdata_test['490']


    skdata_y_train = skdata[target_variables]
    skdata_y_test = skdata_test[target_variables]

    return skdata[ALL_BANDS_C2X], skdata_test[ALL_BANDS_C2X], skdata_y_train,skdata_y_test