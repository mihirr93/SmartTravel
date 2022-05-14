import streamlit as st
import geemap.foliumap as geemap
import geemap.colormaps as cm
from streamlit import session_state as _state
import requests
import json
from requests.structures import CaseInsensitiveDict


import ee
ee.Initialize()


def app():
    st.title("Select your Dream Destination")

    st.markdown(
    """
    Hello! Do you live in Germany and planing your vacation to Maldives even though you can enjoy quite similar landscape in Spain? Or do you live in India and planning your vacation to Switzerland while you can enjoy the same landscape in Kashmir? Would you like to travel to really cool destinations but in a smart and sustainable way? Then use our platform and find out the nearest travel places similar to your dream travel destinations. Select the place in the Map below.
    """
    )
    with st.form("form1"):
        From = st.text_input("Enter your From location")
        To = st.text_input("Enter your Destination location")
        Type = st.selectbox('Select Destination type', ['Mountain', 'Forest', 'Water body','Coast','Island','Dessert','City'])
        Submit = st.form_submit_button(label='Submit')
        #Submit = st.button('Submit')
        if Submit:
            
            url = "https://www.mapquestapi.com/geocoding/v1/address?key=e7u6EurVKAsSsADdVvdwXh2bFhuAMr9D"

            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"

            data = """{"location": "%s"}"""%To
            resp = requests.post(url, headers=headers, data=data)
            data = resp.json()
            lat = data['results'][0]['locations'][0]['latLng']['lat']
            long = data['results'][0]['locations'][0]['latLng']['lng']
            print(lat)
            print(long)
            point = ee.Geometry.Point([long,lat])
            Map = geemap.Map()
            image = (
                ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                .filterBounds(point)
                .filterDate('2019-01-01','2019-12-31')
                .sort('CLOUD_COVER')
                .first()
                .select('B[1-7]')
            )

            vis_params = {'min': 0, 'max': 3000, 'bands': ['B5', 'B4', 'B3']}

            Map.centerObject(point, 10)
            Map.addLayer(image, vis_params, "Landsat-8")
            # Make the training dataset.
            training = image.sample(
                **{
                    #'region': region,
                    'scale': 30,
                    'numPixels': 5000,
                    'seed': 0,
                    'geometries': True,  # Set this to False to ignore geometries
                }
            )
            Map.addLayer(training, {}, 'training', False)
            # Instantiate the clusterer and train it.
            n_clusters = 5
            clusterer = ee.Clusterer.wekaKMeans(n_clusters).train(training)

            # Cluster the input using the trained clusterer.
            result = image.cluster(clusterer)
            # # Display the clusters with random colors.
            Map.addLayer(result.randomVisualizer(), {}, 'clusters', False)
            legend_keys = ['One', 'Two', 'Three', 'Four', 'ect']
            legend_colors = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3']

            # Reclassify the map
            result = result.remap([0, 1, 2, 3, 4], [1, 2, 3, 4, 5])

            Map.addLayer(
                result, {'min': 1, 'max': 5, 'palette': legend_colors}, 'Labelled clusters'
            )
            Map.add_legend(
                legend_keys=legend_keys, legend_colors=legend_colors, position='bottomright'
            )
            Map.to_streamlit(height=700)

        