import datetime
from bokeh.plotting import figure, curdoc
from PIL import Image
import inspect
import textwrap
from urllib.error import URLError
import numpy as np

import pandas as pd
import pydeck as pdk
import streamlit as st

# def show_code(demo):
#     """Show the code of the demo."""
#     show_code = st.sidebar.checkbox("Show code", True)
#     if show_code:
#         # Showing the code of the demo.
#         st.markdown("## Code")
#         sourcelines, _ = inspect.getsourcelines(demo)
#         st.code(textwrap.dedent("".join(sourcelines[1:])))


def mapping_demo():
    @st.cache
    def from_data_file():
        # url = (
        #     "http://raw.githubusercontent.com/streamlit/"
        #     "example-data/master/hello/v1/%s" % filename
        # )
        #DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
        DATA_URL = "data/crops.json"
        json = pd.read_json(DATA_URL)

        return json

    try:

        # Custom color scale
        COLOR_RANGE = [
            [65, 182, 196],
            [127, 205, 187],
            [199, 233, 180],
            [237, 248, 177],
            [255, 255, 204],
            [255, 237, 160],
            [254, 217, 118],
            [254, 178, 76],
            [253, 141, 60],
            [252, 78, 42],
            [227, 26, 28],
            [189, 0, 38],
            [128, 0, 38],
        ]

        BREAKS = [-0.6, -0.45, -0.3, -0.15, 0, 0.15,
                0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2]


        def color_scale(val):
            for i, b in enumerate(BREAKS):
                if val < b:
                    return COLOR_RANGE[i]
            return COLOR_RANGE[i]

        json = from_data_file()
        df = pd.DataFrame()
        # Parse the geometry out in Pandas
        df["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
        df["crop"] = json["features"].apply(lambda row: row["properties"]["crop"])
        df["yield"] = json["features"].apply(lambda row: row["properties"]["yield"])
        df["fill_color"] = json["features"].apply(lambda row: color_scale(row["properties"]["yield"]))

        LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324],[-123.306, 49.324], [-123.306, 49.196]]]

        ALL_LAYERS = {
            "Example dataset": pdk.Layer(
                "PolygonLayer",
                data=df,
                id="geojson",
                opacity=0.8,
                stroked=True,
                get_polygon="coordinates",
                filled=True,
                extruded=False,
                wireframe=True,
                get_fill_color="fill_color",
                get_line_color=[255, 255, 255],
                auto_highlight=False,
                pickable=False,
            )
        }
        st.sidebar.markdown("### Select Crop")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/satellite-v9",
                    initial_view_state={
                        "latitude": 37.574821,
                        "longitude": -5.857086,
                        "zoom": 13
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


### Bokeh
y = np.random.rand(200)

y_2 = np.random.rand(200)

start = datetime.datetime.strptime("21-06-2017", "%d-%m-%Y")
dates = [start]
for _ in y:
    new_date = dates[-1] + datetime.timedelta(days=6)
    dates.append(new_date)

p = figure(
    title='Index Average of selected crops',
    x_axis_label='Date',
    y_axis_label='Index value', 
    height=250, toolbar_location="above", x_axis_type="datetime")

p.line(dates, y, legend_label='NDWI', line_width=1, color="green")

p.line(dates, y_2, legend_label='NDMI', line_width=1, color="red")


doc = curdoc()
doc.theme = 'night_sky'
doc.add_root(p)

#### Streamlit app
st.set_page_config(page_title="Cropernicus Dashboard", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

## Sidebar
st.sidebar.image('img/datafrom.jpg', width=300)

st.sidebar.markdown("# Cropernicus Dashboard")
st.sidebar.write(
    """Commodity traders, seed and fertilizer industry forecast the yield/necessities of any crop production based on local state-owned agencies’ monthly reports. 

For example: an industry commodity leader, Archer Daniels Midlands, on their weekly report, needs to digest USDA’s National Agricultural Statistics Service’s monthly crop predictions, based on past rainfall. 

Our solution predicts crop production using satellite data, providing daily updated information about any given area and commodity. 

Scientific literature and our early machine learning model show a good correlation between Sentinel-2 data, water availability and past crop yields. We are training our model to forecast production based on this newly-available technology. 

Our competitive advantage is giving independent real-time future yield predictions to stakeholders in an easy-to-consume way."""

)


## Main Content
#st.markdown("# Cropernicus Dashboard")
image = Image.open('img/logo.png')
st.image(image, width=500)
st.write(
    """This demo shows how to use the cropernicus dashboard to check for crop yield forecast over time."""
)

image2 = Image.open('img/colormap2.png')
st.image(image2, width=200)

mapping_demo()

st.markdown("Here you can find related indices extracted from Sentinel-2 products.")

st.bokeh_chart(p, use_container_width=True)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# st.markdown("[Cropernicus.com]()")
