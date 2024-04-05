import pandas as pd

def apply_mode_split(mode_split_application_file, pred_trips):

    df = pd.read_csv(mode_split_application_file)

    df['PRIVATE_UTILITY'] = df['PRIVATE_TRAVEL_TIME']*-0.110075 + df['PRIVATE_FARE']*-0.137794 + df['PRIVATE_TAX']*-0.137794
    df['SHARED_UTILITY'] = -0.573322 + df['SHARED_TRAVEL_TIME']*-0.110075 + df['SHARED_FARE']*-0.137794 + df['SHARED_TAX']*-0.137794 + df['HHLDS_MEDIAN_INCOME_ORIGIN_10k']*-0.68228 + df['HHLDS_MEDIAN_INCOME_DESTINAATION_10k']*-0.049448 + df['AIRPORT_FLAGGER']*-2.716947

    df['PRIVATE_PROBABILITY'] = np.exp(df['PRIVATE_UTILITY'])/(np.exp(df['PRIVATE_UTILITY'])+np.exp(df['SHARED_UTILITY']))

    df = df.merge(pred_trips, how = 'left', on = ['ORIGIN','DESTINATION','MONTH', 'YEAR', 'TOD'])
    
    df['PRED_PRIVATE_TRIPS'] = df['PRIVATE_PROBABILITY']*df['PRED_TRIPS']
    df['PRED_SHARED_TRIPS'] = df['PRED_TRIPS'] - df['PRIVATE_TRIPS']

    return df