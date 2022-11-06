from PIL import Image
import inspect
import textwrap
from urllib.error import URLError

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
        DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
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
        df["valuePerSqm"] = json["features"].apply(lambda row: row["properties"]["valuePerSqm"])
        df["growth"] = json["features"].apply(lambda row: row["properties"]["growth"])
        df["fill_color"] = json["features"].apply(lambda row: color_scale(row["properties"]["growth"]))

        LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324],[-123.306, 49.324], [-123.306, 49.196]]]

        ALL_LAYERS = {
            "Area hydrologic": pdk.Layer(
                "PolygonLayer",
                data=LAND_COVER,
                stroked=False,
                # processes the data as a flat longitude-latitude pair
                get_polygon="-",
                get_fill_color=[0, 0, 0, 20],
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
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 49.254, 
                        "longitude": -123.13,
                        "zoom": 11
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


st.set_page_config(page_title="Cropernicus Dashboard", page_icon="🌍")
st.markdown("# Cropernicus Dashboard")
image = Image.open('img/logo.png')

st.image(image, caption='Logo')
st.write(
    """This demo shows how to use the agroboad terminal to check for crop predictions over time. It uses the
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)

mapping_demo()