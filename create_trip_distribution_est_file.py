


#CONSTANTS
EMPTY_PATH = 'Inputs/Empty_Chicago_Matrix.csv'
DEST_CHOICE_MATRIX_PATH = 'Inputs/Destination Choice Model Matricies.csv'
YEARS = [2018,2019,2020]


def assign_data(row, data):
    row = row.append(data.loc[row['ORIGIN']])
    return row
    
empty = pd.read_csv(EMPTY_FILE, index_col = 0 )


df2 = pd.DataFrame()
airport_list = [17031980000,17031980100]
tou

for year in years:
    print('Working on Year '+ (str(year)))
    if year == 2018:
        months = [11,12]
    elif year == 2019:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif year == 2020:
        months = [1,2]
    else:
        print('Bad Year')
        
    for month in months:
        print('Working on Month '+ (str(month)))
    
        for tod in tods:
            print('Working on TOD '+ (str(tod)))
			
            ls = pd.read_csv(DEST_CHOICE_MATRIX_PATH + '/Log Sum/Log_Sum_'+ str(year) + '_' + str(month) + '_' + str(tod) + '.csv', index_col = 0)
            dropoffs = pd.read_csv(DEST_CHOICE_MATRIX_PATH + '/Estimated Dropoffs/' + str(year) + '_' + str(month) + '_' + str(tod) + '_Dropoffs.csv', index_col = 0)

            df = empty.merge(dropoffs, on = ['YEAR','MONTH','TOD','ORIGIN','DESTINATION'])
            df = df.merge(ls[['YEAR','MONTH','TOD','ORIGIN','DESTINATION','LOG_SUM']], on = ['YEAR','MONTH','TOD','ORIGIN','DESTINATION'])

            df2 = df2.append(df)

dist = pd.read_csv('Distance_Matrix.csv')
df2 = df2.merge(dist, on = ['ORIGIN','DESTINATION'])            

df2['INTERNAL_FLAGGER'] = np.where(df2['ORIGIN'] == df2['DESTINATION'],1,0)
df2['AIRPORT_FLAGGER'] = np.where(df2['DESTINATION'].isin(airport_list),1,0)
df2['TOURIST_FLAGGER'] = np.where(df2['DESTINATION'].isin(tourist_list),1,0)
df2['LOG_SUM_AIRPORTS'] = df2['LOG_SUM']*df2['AIRPORT_FLAGGER']
df2['LOG_SUM_NO_AIRPORTS'] = df2['LOG_SUM']*(1-df2['AIRPORT_FLAGGER'])