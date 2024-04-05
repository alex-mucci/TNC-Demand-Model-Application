import numpy as np
import pandas as pd

def apply_trip_generation(tod1_file, tod2_file, tod3_file, tod4_file, tod5_file, weekdays_csv):

	##read in the files
	df1 = pd.read_csv(tod1_file, index_col = 0)
	df2 = pd.read_csv(tod2_file, index_col = 0)
	df3 = pd.read_csv(tod3_file, index_col = 0)
	df4 = pd.read_csv(tod4_file, index_col = 0)
	df5 = pd.read_csv(tod5_file, index_col = 0)


	##apply linear models
	df1['LINEAR_PICKUPS'] = 0.1251485*df1['FOOD_EMP'] + 260.4035*df1['AIR_F'] + 0.0055992*df1['LOW_INC_0'] + 0.1456829*df1['HI_INC_0'] + 0.0206288*df1['LOW_INC_1P'] 
	df1['LINEAR_PICKUPS_LOG'] =  np.where(df1['LINEAR_PICKUPS'] == 0, 0, np.log(df1['LINEAR_PICKUPS']))

	df2['LINEAR_PICKUPS'] = 0.0000952*df2['OTHER_EMP'] + 0.0473473*df2['FOOD_EMP'] + 0.015827*df2['RETAIL_EMP'] + 130.2076*df2['AIR_F'] + 53.18332*df2['TOR_F'] + 0.3745288*df2['HI_INC_0'] + 0.0174729*df2['LOW_INC_0'] + 0.0176063*df2['LOW_INC_1P'] + 0.0000136*df2['HI_INC_1P'] 
	df2['LINEAR_PICKUPS_LOG'] =  np.where(df2['LINEAR_PICKUPS'] == 0, 0, np.log(df2['LINEAR_PICKUPS']))

	df3['LINEAR_PICKUPS'] = 0.1485942*df3['FOOD_EMP'] + 0.0653171*df3['RETAIL_EMP'] + 0.0075034*df3['OTHER_EMP'] + 921.3699*df3['AIR_F'] + 173.4502*df3['TOR_F'] + 0.6336939*df3['HI_INC_0'] + 0.0275177*df3['LOW_INC_0'] + 0.0235304*df3['LOW_INC_1P'] + 0.0000243*df3['HI_INC_1P'] 
	df3['LINEAR_PICKUPS_LOG'] =  np.where(df3['LINEAR_PICKUPS'] == 0, 0, np.log(df3['LINEAR_PICKUPS']))

	df4['LINEAR_PICKUPS'] = 0.1094589*df4['FOOD_EMP'] + 0.0385694*df4['RETAIL_EMP'] + 0.0079508*df4['OTHER_EMP'] + 213.2107*df4['AIR_F'] + 102.1033*df4['TOR_F'] + 0.4440004*df4['HI_INC_0'] + 0.0060732*df4['LOW_INC_0'] + 0.0072242*df4['LOW_INC_1P'] + 0.0000164*df4['HI_INC_1P'] 
	df4['LINEAR_PICKUPS_LOG'] = np.where(df4['LINEAR_PICKUPS'] == 0, 0, np.log(df4['LINEAR_PICKUPS']))

	df5['LINEAR_PICKUPS'] = 0.002725*df5['OTHER_EMP'] + 0.1846295*df5['FOOD_EMP'] + 476.2219*df5['AIR_F'] + 0.350088*df5['HI_INC_0'] + 0.00000446*df5['HI_INC_1P'] + 0.0070386*df5['LOW_INC_0'] + 0.0076753*df5['LOW_INC_1P']
	df5['LINEAR_PICKUPS_LOG'] =  np.where(df5['LINEAR_PICKUPS'] == 0, 0, np.log(df5['LINEAR_PICKUPS']))


	##apply negative binomial models
	df1['PRED_AVG_WD_PICKUPS'] = np.exp(-1.699553*df1['AIR_F'] + 0.5047479*df1['TOR_F'] + 0.3486627*df1['LINEAR_PICKUPS_LOG'] + 1.082214*df1['LOGSUM'] - 0.0173114*df1['MEDIAN_AGE'] + 0.0170123*df1['P_BACH_25P'] + 0.000000716*df1['TOTAL_EMP_DEN'] - 0.028017*df1['DEC_18'] + 0.0220474*df1['JAN_19'] + 0.0560024*df1['FEB_19'] + 0.1222571*df1['MAR_19'] + 0.0544462*df1['APR_19'] + 0.0958898*df1['MAY_19'] + 0.2011476*df1['JUN_19'] + 0.217121*df1['JUL_19'] + 0.2087327*df1['AUG_19'] + 0.1676383*df1['SEP_19'] + 0.1657967*df1['OCT_19'] + 0.2471665*df1['NOV_19'] + 0.2644915*df1['DEC_19'] + 0.2964904*df1['JAN_20'] + 0.2991526*df1['FEB_20'] - 5.691818)

	df2['PRED_AVG_WD_PICKUPS'] = np.exp(-0.7743786*df2['AIR_F'] + 0.4779832*df2['TOR_F'] + 0.4050372*df2['LINEAR_PICKUPS_LOG'] + 0.6230226*df2['LOGSUM'] - 0.0262*df2['MEDIAN_AGE'] + 0.0143772*df2['P_BACH_25P']+ 0.000000498*df1['TOTAL_EMP_DEN'] - 0.0563335*df2['DEC_18'] + 0.0918763*df2['JAN_19'] + 0.2369338*df2['FEB_19'] + 0.2762176*df2['MAR_19'] + 0.1257616*df2['APR_19'] + 0.100636*df2['MAY_19'] - 0.0465612*df2['JUN_19'] - 0.0191302*df2['JUL_19'] + 0.0155422*df2['AUG_19'] + 0.1303734*df2['SEP_19'] + 0.1265867*df2['OCT_19'] + 0.1615657*df2['NOV_19'] + 0.101676*df2['DEC_19'] + 0.2673337*df2['JAN_20'] + 0.3775664*df2['FEB_20'] - 1.946639)

	df3['PRED_AVG_WD_PICKUPS'] = np.exp(-0.6405087*df3['AIR_F'] + 0.7809523*df3['TOR_F'] + 0.3927277*df3['LINEAR_PICKUPS_LOG'] + 0.6977969*df3['LOGSUM'] - 0.0208753*df3['MEDIAN_AGE'] + 0.0123951*df3['P_BACH_25P']+ 0.00000161*df1['TOTAL_EMP_DEN'] - 0.0390817*df3['DEC_18'] + 0.098963*df3['JAN_19'] + 0.2032421*df3['FEB_19'] + 0.2396192*df3['MAR_19'] + 0.1364222*df3['APR_19'] + 0.1078783*df3['MAY_19'] + 0.146028*df3['JUN_19'] + 0.1585698*df3['JUL_19'] + 0.1623656*df3['AUG_19'] + 0.1184939*df3['SEP_19'] + 0.1605051*df3['OCT_19'] + 0.2076105*df3['NOV_19'] + 0.189735*df3['DEC_19'] + 0.2911973*df3['JAN_20'] + 0.3918755*df3['FEB_20'] - 2.551229)

	df4['PRED_AVG_WD_PICKUPS'] = np.exp(-0.4855696*df4['AIR_F'] + 0.890186*df4['TOR_F'] + 0.4090155*df4['LINEAR_PICKUPS_LOG'] + 0.8352944*df4['LOGSUM'] - 0.0216488*df4['MEDIAN_AGE'] + 0.0149257*df4['P_BACH_25P']+ 0.00000217*df1['TOTAL_EMP_DEN'] - 0.0307113*df4['DEC_18'] + 0.0641547*df4['JAN_19'] + 0.1974895*df4['FEB_19'] + 0.2202914*df4['MAR_19'] + 0.0553759*df4['APR_19'] + 0.0594408*df4['MAY_19'] + 0.0540622*df4['JUN_19'] + 0.0249321*df4['JUL_19'] + 0.0376746*df4['AUG_19'] + 0.056278*df4['SEP_19'] + 0.0935998*df4['OCT_19'] + 0.1979503*df4['NOV_19'] + 0.1853279*df4['DEC_19'] + 0.2399905*df4['JAN_20'] + 0.363544*df4['FEB_20'] - 4.089885)

	df5['PRED_AVG_WD_PICKUPS'] = np.exp(0.0188928*df5['AIR_F'] + 0.830838*df5['TOR_F'] + 0.3445732*df5['LINEAR_PICKUPS_LOG'] + 0.9817033*df5['LOGSUM'] - 0.0215845*df5['MEDIAN_AGE'] + 0.0199614*df4['P_BACH_25P']+ 0.00000224*df1['TOTAL_EMP_DEN'] - 0.021861*df5['DEC_18'] + 0.0234194*df5['JAN_19'] + 0.1784418*df5['FEB_19'] + 0.2219709*df5['MAR_19'] + 0.0799116*df5['APR_19'] + 0.0603504*df5['MAY_19'] + 0.1119321*df5['JUN_19'] + 0.097184*df5['JUL_19'] + 0.1199707*df5['AUG_19'] + 0.1197228*df5['SEP_19'] + 0.148494*df5['OCT_19'] + 0.2136709*df5['NOV_19'] + 0.256858*df5['DEC_19'] + 0.2785087*df5['JAN_20'] + 0.4076045*df5['FEB_20'] - 5.265743)

	#append all of the tod specific dataframes together
	pred_trips = df1.append(df2)
	pred_trips = df1.append(df3)
	pred_trips = df1.append(df4)
	pred_trips = df1.append(df5)

	#convert average weekday trips to monthly trip totals
	wd = pd.read_csv(weekdays_csv)
	pred_trips = pred_trips.merge(wd, on = ['MONTH','YEAR'])
	
	return pred_trips