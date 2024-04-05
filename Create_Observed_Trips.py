import pandas as pd
import numpy as np


def create_observed_trips(tods, years, h5_file, weekdays_csv, output):
	df_all = pd.DataFrame()

	for year in years:
		print('Working on year ' + str(year))
		if year == 2018:
			months = [11,12]
		elif year == 2020:
			months = [1,2]
		else:
			months = [1,2,3,4,5,6,7,8,9,10,11,12]
			
		for month in months:
			print('Working on month ' + str(month))
			
			for tod in tods:
				print('Working on tod ' + str(tod))

				store = pd.HDFStore(h5_file)
				df = store.select(where = ['YEAR == ' + str(year), 'MONTH == ' + str(month)], key = 'Weekday_' + str(tod))
				store.close()

				df['TOD'] = tod

				df = df[df['TRIP_LENGTH_MILES'] <= 50]
				df = df[df['TRAVEL_TIME_MINUTES'] <= 120]

				#drop the trips that have a trip length of 0 or travel time of 0 because they do not make sense
				df = df[df['TRIP_LENGTH_MILES'] > 0]
				df = df[df['TRAVEL_TIME_MINUTES'] > 0]

				#filter out the trips that have an unreasonable speed
				df = df[df['SPEED']<120]

				print('Maximum Travel Time')
				print(df['TRAVEL_TIME_MINUTES'].max())

				print('Maximum Trip Length')
				print(df['TRIP_LENGTH_MILES'].max())

				print('Maximum Speed')
				print(df['SPEED'].max())


				#census tract 17031980000 replaces the trips assigned to census tract 17031770700 because they are likely misasigned.
				#Census tract 17031980000 contains contains O'Hare airport and census tract is adjacent. The trips assigned to census tract 17031770700 are likely trips from the airport.
				df.loc[df['ORIGIN'] == 17031770700, 'ORIGIN'] = 17031980000
				df.loc[df['DESTINATION'] == 17031770700, 'DESTINATION'] = 17031980000


				df = df[df['EXTERNAL_FLAGGER'] == 0]
				df = df[df['INTERNAL_EXTERNAL_FLAGGER'] == 0]


				df['PRIVATE_TRIPS'] = np.where(df['SHARED_FLAGGER'] == 0, 1,0)
				df['SHARED_TRIPS'] = np.where(df['SHARED_FLAGGER'] == 1, 1,0)
				
				df['MATCHED_TRIPS'] = np.where(df['NUM_TRIPS_POOLED'] > 1, 1,0)
				df['UNMATCHED_TRIPS'] =  df['SHARED_TRIPS'] - df['MATCHED_TRIPS']

				df['TRIPS'] = 1

				df = df.groupby(by= ['ORIGIN','DESTINATION','YEAR', 'MONTH','TOD'], as_index =False).sum()

				df_all = df_all.append(df)

	df_all = df_all.groupby(by= ['ORIGIN','DESTINATION','YEAR', 'MONTH','TOD'], as_index = False).sum()

	weekday = pd.read_csv(weekdays_csv)


	df2 = df_all.merge(weekday, on = ['YEAR','MONTH'])


	df2['AVG_WD_TRIPS'] = df2['TRIPS']/df2['WEEKDAYS']
	df2['AVG_WD_PRIVATE_TRIPS'] = df2['PRIVATE_TRIPS']/df2['WEEKDAYS']
	df2['AVG_WD_SHARED_TRIPS'] = df2['SHARED_TRIPS']/df2['WEEKDAYS']
	df2['AVG_WD_MATCHED_TRIPS'] = df2['MATCHED_TRIPS']/df2['WEEKDAYS']
	df2['AVG_WD_UNMATCHED_TRIPS'] = df2['UNMATCHED_TRIPS']/df2['WEEKDAYS']

	agg = {'TRIPS':'sum','WEEKDAYS':'first'}
    
	print('Writting File to Output')

	df2[['ORIGIN', 'DESTINATION', 'YEAR', 'MONTH','TOD','PRIVATE_TRIPS','SHARED_TRIPS', 'MATCHED_TRIPS', 'UNMATCHED_TRIPS', 'TRIPS', 'WEEKDAYS']].to_csv(output)

	return df2