import pandas as pd
import numpy as np
import folium
import geopandas as gp

def viz_trip_generation(est_file, maps_output, tracts_shapefile,tods):
    ##make choropleth maps
    geo = gp.read_file(tracts_shapefile)
    geo['geoid10'] = geo.geoid10.astype(float)

    for tod in tods:
        if tod == 1:
            df = est_file[est_file['TOD'] == 1]
        elif tod ==2:
            df = est_file[est_file['TOD'] == 2]
        elif tod ==3:
            df = est_file[est_file['TOD'] == 3]
        elif tod ==4:
            df = est_file[est_file['TOD'] == 4]
        elif tod ==5:
            df = est_file[est_file['TOD'] == 5]
        else:
            print('Bad TOD')
        
        
        df = df.groupby(by = ['ORIGIN'], as_index = False).sum()
        df['DIFF'] = df['PRED_AVG_WD_PICKUPS'] - df['AVG_WD_PICKUPS']

    ###make observed pickup maps for each tod
        m = folium.Map([41.8781, -87.6298], zoom_start=11)
        m.choropleth(
         geo_data=geo,
         name= 'TOD ' + str(tod) + ' Observed Pickups',
         data= df,
         columns= ['ORIGIN', 'AVG_WD_PICKUPS'],
         key_on= 'feature.properties.geoid10',
         fill_color= 'RdPu',
         fill_opacity= 0.6,
         line_opacity= 0.2,
         legend_name=  'Observed Pickups',
         highlight = True
        )

        folium.LayerControl().add_to(m)

        m.save(maps_output + 'TOD_' + str(tod) + '_Observed_Pickups.html')


    ###make predicted pickup maps for each tod 
        m = folium.Map([41.8781, -87.6298], zoom_start=11)

        m.choropleth(
         geo_data=geo,
         name= 'TOD ' + str(tod) + ' Predicted Pickups',
         data=df,
         columns = ['ORIGIN', 'PRED_AVG_WD_PICKUPS'],
         key_on='feature.properties.geoid10',
         fill_color='RdPu',
         fill_opacity=0.6,
         line_opacity=0.2,
         legend_name='Predicted Pickups',
         highlight = True
        )

        folium.LayerControl().add_to(m)

        m.save(maps_output + 'TOD_' + str(tod) + '_Predicted_Pickups.html')


    ###make accuracy maps for each tod
     
        m = folium.Map([41.8781, -87.6298], zoom_start=11)
        
        if tod == 1:
            bins = [-10,-5,-1, 1, 5, 10]
        elif tod == 2:
            bins = [-10,-5,-1, 1, 5, 10]
        elif tod == 3:
            bins = [-20, -5, -1, 1, 5, 20]
        elif tod == 4:
            bins = [-20, -5, -1, 1, 5, 20]
        elif tod == 5:
            bins = [-30, -10, -1, 1, 10, 30]
        else:
            print('Bad TOD')

        m.choropleth(
         geo_data=geo,
         name= 'TOD ' + str(tod) + ' Trip Generation Model Accuracy',
         data=df,
         columns = ['ORIGIN', 'DIFF'],
         key_on='feature.properties.geoid10',
         fill_color='RdYlGn',
         fill_opacity=0.6,
         line_opacity=0.2,
         #bins = bins,
         legend_name='Difference Pickups',
         highlight = True
        )

        folium.LayerControl().add_to(m)

        m.save(maps_output + 'TOD_' + str(tod) +'_Pickups_Diff.html')

    df = est_file.groupby(by = ['ORIGIN'], as_index = False).sum()
    df['DIFF'] = df['PRED_AVG_WD_PICKUPS'] - df['AVG_WD_PICKUPS']
    print('The minimum difference is ' + str(df['DIFF'].min()))
    print('The average difference is ' + str(df['DIFF'].mean()))
    print('The maximum difference is ' + str(df['DIFF'].max()))

    # make observed pickup maps for all day
    m = folium.Map([41.8781, -87.6298], zoom_start=11)
    m.choropleth(
     geo_data=geo,
     name= 'All Day Observed Pickups',
     data= df,
     columns= ['ORIGIN', 'AVG_WD_PICKUPS'],
     key_on= 'feature.properties.geoid10',
     fill_color= 'RdPu',
     fill_opacity= 0.6,
     line_opacity= 0.2,
     legend_name= 'Observed Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)

    m.save(maps_output + 'All_Day_Observed_Pickups.html')


    # make predicted pickup map for all day 
    m = folium.Map([41.8781, -87.6298], zoom_start=11)

    m.choropleth(
     geo_data=geo,
     name= 'All Day Predicted Pickups',
     data=df,
     columns = ['ORIGIN', 'PRED_AVG_WD_PICKUPS'],
     key_on='feature.properties.geoid10',
     fill_color='RdPu',
     fill_opacity=0.6,
     line_opacity=0.2,
     legend_name='Predicted Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)

    m.save(maps_output + 'All_Day_Predicted_Pickups.html')


    # make accuracy map for all day

    m = folium.Map([41.8781, -87.6298], zoom_start=11)

    if tod == 1:
        bins = [-10,-5,-1, 1, 5, 10]
    elif tod == 2:
        bins = [-10,-5,-1, 1, 5, 10]
    elif tod == 3:
        bins = [-20, -5, -1, 1, 5, 20]
    elif tod == 4:
        bins = [-20, -5, -1, 1, 5, 20]
    elif tod == 5:
        bins = [-30, -10, -1, 1, 10, 30]
    else:
        print('Bad TOD')

    m.choropleth(
     geo_data=geo,
     name= 'All Day Trip Generation Model Accuracy',
     data=df,
     columns = ['ORIGIN', 'DIFF'],
     key_on='feature.properties.geoid10',
     fill_color='RdYlGn',
     fill_opacity=0.6,
     line_opacity=0.2,
    #bins = bins,
     legend_name='Difference Pickups',
     highlight = True
    )

    folium.LayerControl().add_to(m)
    
    m.save(maps_output + 'All_Day_Pickups_Diff.html')
