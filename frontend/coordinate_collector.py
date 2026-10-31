
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os

st.set_page_config(
    page_title="Campus Coordinate Collector",
    layout="wide"
)

st.title("Smart Campus - Coordinate Collector")
st.write("Select a campus location and click its exact position on the map.")

# All 26 locations from your graph
locations = [
    "Main Gate",
    "Admin Block",
    "B-tech Block",
    "Santoshanand Library",
    "Gate 2",
    "Gate 3",
    "CSIT Tuckshop",
    "Chanakya Tuckshop",
    "B-tech Tuckshop",
    "Ravi Canteen",
    "CSIT Block",
    "Chanakya Block",
    "KP Nautiyal Block",
    "Old MCA Block",
    "Mechanical Block",
    "Civil Block",
    "Electrical Block",
    "Paramedical Block",
    "Convocation Centre",
    "Aryabhatta Lab",
    "Param Lab",
    "Happiness Cafe",
    "Quick Bite Cafe",
    "Main Ground",
    "Basketball Court",
    "Badminton Court"
]

# Approximate campus centre
CENTER = [30.2679993, 77.9960119]

# Store collected coordinates
if "coordinates" not in st.session_state:
    st.session_state.coordinates = {}

selected_location = st.selectbox(
    "Choose a location",
    locations
)

st.write("Click the corresponding building or facility on the map.")

campus_map = folium.Map(
    location=CENTER,
    zoom_start=18,
    tiles="OpenStreetMap"
)

# Show previously collected markers
for name, coords in st.session_state.coordinates.items():
    folium.Marker(
        location=coords,
        popup=name,
        tooltip=name
    ).add_to(campus_map)

map_result = st_folium(
    campus_map,
    height=550,
    width=None,
    key="campus_coordinate_map"
)

if map_result and map_result.get("last_clicked"):
    clicked = map_result["last_clicked"]

    st.write(
        f"Selected coordinates: "
        f"{clicked['lat']}, {clicked['lng']}"
    )

    if st.button("Save coordinates for " + selected_location):
        st.session_state.coordinates[selected_location] = [
            clicked["lat"],
            clicked["lng"]
        ]
        st.success(f"{selected_location} coordinates saved!")
        st.rerun()

st.divider()

st.subheader("Collected Locations")

st.write(
    f"Completed: {len(st.session_state.coordinates)} "
    f"/ {len(locations)}"
)

if st.session_state.coordinates:
    st.json(st.session_state.coordinates)

    if st.button("Download coordinates JSON"):
        data = json.dumps(
            st.session_state.coordinates,
            indent=4
        )

        st.download_button(
            "Download JSON file",
            data=data,
            file_name="campus_coordinates.json",
            mime="application/json"
        )
else:
    st.info("No coordinates collected yet.")
