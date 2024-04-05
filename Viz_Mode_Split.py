import folium
import geopandas as gp

def vix_mode_split(pred, obs, output):

	#create choropleth maps
	map_df = pd.merge(pred, obs[['MONTH','YEAR','TOD','ORIGIN','DESTINATION','AVG_WD_PRIVATE_TRIPS', 'AVG_WD_SHARED_TRIPS']], how = 'left', on = ['MONTH','YEAR','TOD','ORIGIN','DESTINATION'])
	map_df = map_df['AVG_WD_PRIVATE_TRIPS'].fillna(0)
	map_df = map_df['AVG_WD_SHARED_TRIPS'].fillna(0)

	#create observed drop offs map for each tod
	m = folium.Map([41.8781, -87.6298], zoom_start=11)
	   
    df = df_map
    agg = {'PRED_TRIPS':'sum','GEOID10_STR':'first','AVG_WD_PRIVATE_TRIPS':'sum','AVG_WD_SHARED_TRIPS':'sum','TOD':'first'}
    df = df['DESTINATION','PRED_TRIPS','GEOID10_STR','AVG_WD_PRIVATE_TRIPS','AVG_WD_SHARED_TRIPS','TOD']].groupby(by = ['DESTINATION'], as_index = False).agg(agg)
    df['PRIVATE_DIFF'] = df['PRED_PRIVATE_TRIPS'] - df['AVG_WD_PRIVATE_TRIPS']
    df['SHARED_DIFF'] = df['PRED_SHARED_TRIPS'] - df['AVG_WD_SHARED_TRIPS']

    m.choropleth(
     geo_data=geo,
     name= 'Observed Private Pickups',
     data=df,
     columns = ['ORIGIN', 'AVG_WD_PRIVATE_TRIPS'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    m.save(output + 'Obs_Privte_Pickups.html')
    
    
    m.choropleth(
     geo_data=geo,
     name= 'Observed Shared Pickups',
     data=df,
     columns = ['ORIGIN', 'AVG_WD_SHARED_TRIPS_TRIPS'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    m.save(output + 'Obs_Shared_Pickups.html')
    
    
    #create predicted mode specific pickups map 
    m = folium.Map([41.8781, -87.6298], zoom_start=11)
   
    m.choropleth(
     geo_data=geo,
     name= 'Predicted Private Pickups',
     data=df,
     columns = ['ORIGIN', 'PRED_PRIVATE_TRIPS'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    m.save(output + 'Pred_Private_Pickups.html')
    
    
    #create private trips diff map 
    m = folium.Map([41.8781, -87.6298], zoom_start=11)
   

    m.choropleth(
     geo_data=geo,
     name= 'Mode Split Model Accuracy',
     data=df,
     columns = ['ORIGIN', 'PRIVATE_DIFF'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Private Pickups Difference',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    m.save(output + 'Mode_Split_Private_Diff.html')
    
   
    #create private mode share diff for each tod
    m = folium.Map([41.8781, -87.6298], zoom_start=11)
   
   
    df['OBS_PRIVATE_MODE_SHARE'] = df['AVG_WD_PRIVATE_TRIPS']/(df['AVG_WD_SHARED_TRIPS_TRIPS'] + df['AVG_WD_PRIVATE_TRIPS']
    df['PRED_PRIVATE_MODE_SHARE'] = df['PRED_PRIVATE_TRIPS']/(df['PRED_SHARED_TRIPS'] + df['PRED_PRIVATE_TRIPS']
    df['PRIVATE_MODE_SHARE_DIFF'] = df['PRED_PRIVATE_MODE_SHARE'] - df['OBS_PRIVATE_MODE_SHARE']

    m.choropleth(
     geo_data=geo,
     name= 'Mode Split Model Accuracy',
     data=df,
     columns = ['ORIGIN', 'PRIVATE_MODE_SHARE_DIFF'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Private Pickups Difference',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    m.save(output + 'Mode_Split_Private_Diff.html')
   