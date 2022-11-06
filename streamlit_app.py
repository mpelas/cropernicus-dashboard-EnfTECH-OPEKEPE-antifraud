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
        CATTLE_DATA = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_cattle.csv"
        cattle_df = pd.read_csv(CATTLE_DATA, header=None)

        return cattle_df #pd.read_json(url)

    try:

        data = from_data_file()

        HEADER = ["lng", "lat", "weight"]
        data.columns = HEADER

        #view = pdk.data_utils.compute_view(data[["lng", "lat"]])
        p75, p90, p99 = data["weight"].quantile([0.75, 0.9, 0.99])

        STROKE_WIDTH = 5
        CELL_SIZE = 3000

        CONTOURS_0 = [
            {"threshold": p75, "color": [
                0, 238, 224], "strokeWidth": STROKE_WIDTH},
            {"threshold": p90, "color": [
                0, 180, 240], "strokeWidth": STROKE_WIDTH},
            {"threshold": p99, "color": [0, 0, 240],
                "strokeWidth": STROKE_WIDTH},
        ]


        ALL_LAYERS = {
            "Area hydrologic": pdk.Layer(
                "ContourLayer",
                data=data,
                get_position=["lng", "lat"],
                contours=CONTOURS_0,
                cell_size=CELL_SIZE,
                aggregation=pdk.types.String("MEAN"),
                get_weight="weight",
                pickable=True,
            ),
            "Rice": pdk.Layer(
                "ContourLayer",
                data=data,
                get_position=["lng", "lat"],
                contours=CONTOURS_0,
                cell_size=CELL_SIZE,
                aggregation=pdk.types.String("MEAN"),
                get_weight="weight",
                pickable=True,
            ),
            "Corn": pdk.Layer(
                "ContourLayer",
                data=data,
                get_position=["lng", "lat"],
                contours=CONTOURS_0,
                cell_size=CELL_SIZE,
                aggregation=pdk.types.String("MEAN"),
                get_weight="weight",
                pickable=True,
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
                        "latitude": 37.76,
                        "longitude": -122.4,
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
st.markdown("# Agroboard")
st.write(
    """This demo shows how to use the agroboad terminal to check for crop predictions over time. It uses the
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)

mapping_demo()