import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gp
import folium

from Apply_Trip_Generation import apply_trip_generation
from Viz_Trip_Generation import viz_trip_generation

from Apply_Trip_Distribution import apply_trip_distribution
from Viz_Trip_Distribution import viz_trip_distribution

from Create_Observed_Trips import create_observed_trips

#STEP 1 CONSTANTS
TOD1_FILE = 'Inputs/Trip Generation/Trip_Generation_Origin_Estimation_File_TOD_1.csv'
TOD2_FILE = 'Inputs/Trip Generation/Trip_Generation_Origin_Estimation_File_TOD_2.csv'
TOD3_FILE = 'Inputs/Trip Generation/Trip_Generation_Origin_Estimation_File_TOD_3.csv'
TOD4_FILE = 'Inputs/Trip Generation/Trip_Generation_Origin_Estimation_File_TOD_4.csv'
TOD5_FILE = 'Inputs/Trip Generation/Trip_Generation_Origin_Estimation_File_TOD_5.csv'
TRIP_GEN_MAPS_OUTPUT = 'Outputs/Trip Generation/Maps/'
TRACTS_SHAPEFILE = 'Inputs/geo_export_558aad9f-98d8-4dd5-a6b1-c1730155d596.shp'
TODS = [1,2,3,4,5]
YEARS = [2018, 2019, 2020]
TRIP_GEN_OUTPUT = 'Outputs/Trip Generation/Trip_Generation_Predicted_Pickups.csv'
WEEKDAYS_CSV = 'C:/Workspace/TNC-Demand-Model-Application/Inputs/Number of Weekdays.csv'

H5_FILE = 'C:/Workspace/TNC-Demand-Model/Outputs/Chicago_TNC_Trips_20.H5'
OBSERVED_OUTPUT = 'C:/Workspace/TNC-Demand-Model-Application/Outputs/OBS_AVG_WD_TRIPS.csv'

#STEP 2 CONSTANTS
TRIP_DIST_FILE = 'Inputs/Trip Distribution/Trip_Distribution_Application_File.csv'
WEEKDAYS_PATH = 'Inputs/Trip Distribution/Number of Weekdays.csv'
DOWNTOWN_TRACTS_PATH = 'Inputs/Trip Distribution/Downtown Zone Census Tracts.csv'
TRIP_DIST_MAPS_OUTPUT = 'Outputs/Trip Distribution/Maps/'
TRIP_DIST_OUTPUT = 'Outputs/Trip Distribution/Trip_Distribution_Predicted_Trips.csv'

#STEP 3 CONSTANTS
MODE_SPLIT_FILE = 'Inputs/Mode Split/Mode_Split_Application_File.csv'
MODE_SPLIT_MAPS_OUTPUT = 'Outputs/Mode Split/Maps/'
MODE_SPLIT_OUTPUT = 'Outputs/Mode Split/Mode_Split_Predicted_Trips.csv'


#STEP 1: TRIP GENERATION APPLICATION
print('Working on Trip Generation Step')
pred_trips = apply_trip_generation(TOD1_FILE, TOD2_FILE, TOD3_FILE, TOD4_FILE, TOD5_FILE, WEEKDAYS_CSV)
print('Visualizing Trip Generation Results')
viz_trip_generation(pred_trips, TRIP_GEN_MAPS_OUTPUT, TRACTS_SHAPEFILE,TODS)
print('Creating Observed Trips File')
#obs = create_observed_trips(TODS, YEARS, H5_FILE, WEEKDAYS_CSV, OBSERVED_OUTPUT)
obs = pd.read_csv(OBSERVED_OUTPUT)
print('Writting predicted trips file')
pred_trips.to_csv(TRIP_GEN_OUTPUT)


#STEP 2 TRIP DISTRIBUTION
print('Working on Trip Distribution Step')
pred_trips = apply_trip_distribution(TRIP_DIST_FILE, pred_trips)
viz_trip_distribution(pred_trips, obs, TRIP_DIST_MAPS_OUTPUT)

print('Writting predicted trips file')
pred_trips.to_csv(TRIP_DIST_OUTPUT)



#STEP 3 MODE SPLIT LOGIT MODELS
pred_trips = apply_mode_split(MODE_SPLIT_FILE, pred_trips)
viz_mode_split(pred_trips, obs, MODE_SPLIT_MAPS_OUTPUT)

print('The average number of predicted average weekday private trips is ' + pred_trips['PRIVATE_TRIPS'].mean())
print('The average number of predicted average weekday shared trips is ' + pred_trips['SHARED_TRIPS'].mean())

print('The average number of observed average weekday private trips is ' + obs['OBS_PRIVATE_TRIPS_AVG'].mean())
print('The average number of observed average weekday shared trips is ' + obs['OBS_SHARED_TRIPS_AVG'].mean())


print('Writting predicted trips file')
pred_trips.to_csv(MODE_SPLIT_OUTPUT)




