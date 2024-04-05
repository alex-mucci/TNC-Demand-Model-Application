import numpy as np
import pandas as pd

def apply_trip_distribution(trip_dist_file, trip_gen_pred_trips):
    print('Reading in trip distribution application file')
    df2 = pd.read_csv(trip_dist_file)

    print('Applying trip distribution model')

    df2['UTILITY'] = np.where(df2['TOD'] == 1, np.log(df2['PRED_DROPOFFS']) - 2.81*df2['AIRPORT_FLAGGER'] + 0.49*df2['TOURIST_FLAGGER'] - 0.07*df2['INTERNAL_FLAGGER'] + 0*df2['LOG_SUM_AIRPORTS'] + 1*df2['LOG_SUM_NO_AIRPORTS'], np.nan)
    df2['UTILITY'] = np.where(df2['TOD'] == 2, np.log(df2['PRED_DROPOFFS']) - 2.18*df2['AIRPORT_FLAGGER'] + 0.47*df2['TOURIST_FLAGGER'] - 0.80*df2['INTERNAL_FLAGGER'] + 0.15*df2['LOG_SUM_AIRPORTS'] + 0.85*df2['LOG_SUM_NO_AIRPORTS'], df2['UTILITY'])
    df2['UTILITY'] = np.where(df2['TOD'] == 3, np.log(df2['PRED_DROPOFFS']) - 2.84*df2['AIRPORT_FLAGGER'] + 0.48*df2['TOURIST_FLAGGER'] - 1.22*df2['INTERNAL_FLAGGER'] + 0.08*df2['LOG_SUM_AIRPORTS'] + 0.96*df2['LOG_SUM_NO_AIRPORTS'], df2['UTILITY'])
    df2['UTILITY'] = np.where(df2['TOD'] == 4, np.log(df2['PRED_DROPOFFS']) - 1.95*df2['AIRPORT_FLAGGER'] + 0.23*df2['TOURIST_FLAGGER'] - 1.20*df2['INTERNAL_FLAGGER'] + 0.12*df2['LOG_SUM_AIRPORTS'] + 0.72*df2['LOG_SUM_NO_AIRPORTS'], df2['UTILITY'])
    df2['UTILITY'] = np.where(df2['TOD'] == 5, np.log(df2['PRED_DROPOFFS']) - 2.18*df2['AIRPORT_FLAGGER'] + 0.30*df2['TOURIST_FLAGGER'] - 1.06*df2['INTERNAL_FLAGGER'] + 0.16*df2['LOG_SUM_AIRPORTS'] + 0.91*df2['LOG_SUM_NO_AIRPORTS'], df2['UTILITY'])


    df2['EXP_UTILITY'] = np.exp(df2['UTILITY'])
    util_sum = df2[['ORIGIN','MONTH','YEAR','TOD','EXP_UTILITY']].groupby(by =['ORIGIN','MONTH','YEAR','TOD'],as_index = False).sum()
    df2 = df2.merge(util_sum, how = 'left', on = ['ORIGIN','MONTH','YEAR','TOD'], suffixes = ('','_SUM'))
    df2['SHARE'] = df2['EXP_UTILITY']/df2['EXP_UTILITY_SUM']


    df2 = df2.merge(trip_gen_pred_trips, how = 'left', on = ['ORIGIN','YEAR','MONTH','TOD'])

    df2['PRED_TRIPS'] = df2['PRED_PICKUPS']*df2['SHARE']
    print('The total number of predicted average weekday pickups before the trip distribution application is ' + str(pred_trips['PRED_PICKUPS'].sum()))
    print('The total number of predicted average weekday trips after the trip distribution application is ' + str(df2['PRED_TRIPS'].sum()))
    
    return df2
