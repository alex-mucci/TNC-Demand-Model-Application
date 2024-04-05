import folium
import geopandas as gp

def viz_trip_distribution(pred, obs, output):

	#create choropleth maps
	map_df = pd.merge(pred, obs[['MONTH','YEAR','TOD','ORIGIN','DESTINATION','OBS_TRIPS_AVG']], how = 'left', on = ['MONTH','YEAR','TOD','ORIGIN','DESTINATION'])
	map_df = map_df['OBS_TRIPS_AVG'].fillna(0)


	#create observed drop offs map for each tod
	m = folium.Map([41.8781, -87.6298], zoom_start=11)
	   
	for tod in tods:
		df = map_df[map_df['TOD'] == tod]
		agg = {'PRED_TRIPS':'sum','GEOID10_STR':'first','OBS_TRIPS_AVG':'sum','TOD':'first'}
		df = df[['DESTINATION','PRED_TRIPS','GEOID10_STR','OBS_TRIPS_AVG','TOD']].groupby(by = ['DESTINATION'], as_index = False).agg(agg)
		df['DIFF'] = df['PRED_TRIPS'] - df['OBS_TRIPS_AVG']
        
		m.choropleth(
		 geo_data=geo,
		 name= 'TOD ' + str(tod) + ' Observed Drop Offs',
		 data=df,
		 columns = ['DESTINATION', 'OBS_TRIPS_AVG'],
		 key_on='feature.properties.geoid10',
		 fill_color='RdYlGn',
		 fill_opacity=0.6,
		 line_opacity=0.2,
		 legend_name='Drop Offs',
		 highlight = True
		)

		folium.LayerControl().add_to(m)

		m.save(output + 'TOD_' + str(tod) + '_Obs_Drop_Offs.html')
        
        #create predicted drop offs map for each tod
		m = folium.Map([41.8781, -87.6298], zoom_start=11)
	   

		m.choropleth(
		 geo_data=geo,
		 name= 'TOD ' + str(tod) + ' Predicted Drop Offs',
		 data=df,
		 columns = ['DESTINATION', 'PRED_TRIPS'],
		 key_on='feature.properties.geoid10',
		 fill_color='RdYlGn',
		 fill_opacity=0.6,
		 line_opacity=0.2,
		 legend_name='Drop Offs',
		 highlight = True
		)

		folium.LayerControl().add_to(m)

		m.save(output + 'TOD_' + str(tod) +'_Pred_Drop_Offs.html')
        
        
        #create diff map for each tod
		m = folium.Map([41.8781, -87.6298], zoom_start=11)
	   

		m.choropleth(
		 geo_data=geo,
		 name= 'TOD ' + str(tod) + ' Trip Distribution Model Accuracy',
		 data=df,
		 columns = ['DESTINATION', 'DIFF'],
		 key_on='feature.properties.geoid10',
		 fill_color='RdYlGn',
		 fill_opacity=0.6,
		 line_opacity=0.2,
		 legend_name='Drop Offs Difference',
		 highlight = True
		)

		folium.LayerControl().add_to(m)

		m.save(output + 'TOD_' + str(tod) +'_Drop_Offs_Diff.html')
        
	   
       
    #create all day observed drop offs map
	map_df = map_df.groupby(by = 'DESTINATION', as_index = False).agg(agg)
	map_df['DIFF'] = map_df['PRED_TRIPS'] - map_df['OBS_TRIPS_AVG']
    
	print('The minimum difference is ' + str(map_df['DIFF'].min()))
	print('The average difference is ' + str(map_df['DIFF'].mean()))
	print('The maximum difference is ' + str(map_df['DIFF'].max()))
    
	m = folium.Map([41.8781, -87.6298], zoom_start=11)
	m.choropleth(
	 geo_data=geo,
	 name= 'All Day Observed Drop Offs',
	 data=map_df,
	 columns = ['DESTINATION', 'OBS_TRIPS_AVG'],
	 key_on='feature.properties.geoid10',
	 fill_color='RdYlGn',
	 fill_opacity=0.6,
	 line_opacity=0.2,
	 legend_name='Drop Offs',
	 highlight = True
    )

	folium.LayerControl().add_to(m)

	m.save(output +'All_Day_Obs_Drop_Offs.html')
    
    
    #create all day predicted drop offs map 
	m = folium.Map([41.8781, -87.6298], zoom_start=11)
   
	m.choropleth(
	geo_data=geo,
	name= 'All Day Predicted Drop Offs',
	data=map_df,
	columns = ['DESTINATION', 'PRED_TRIPS'],
	key_on='feature.properties.geoid10',
	fill_color='RdYlGn',
	fill_opacity=0.6,
	line_opacity=0.2,
	legend_name='Drop Offs',
	highlight = True
	)

	folium.LayerControl().add_to(m)

	m.save(output + 'All_Day_Pred_Drop_Offs.html')
    
    
    #create all day diff map 
	m = folium.Map([41.8781, -87.6298], zoom_start=11)
   
	m.choropleth(
	geo_data=geo,
	name= 'All Day Trip Distribution Model Accuracy',
	data=map_df,
	columns = ['DESTINATION', 'DIFF'],
	key_on='feature.properties.geoid10',
	fill_color='RdYlGn',
	fill_opacity=0.6,
	line_opacity=0.2,
	legend_name='Drop Offs Difference',
	highlight = True
	)

	folium.LayerControl().add_to(m)

	m.save(output + 'All_Day_Drop_Offs_Diff.html')     