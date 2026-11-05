
import json
import sys
from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from campus_coordinates import campus_coordinates

ENTRANCES_FILE = BACKEND_DIR / "entrances.json"


# --------------------------------------------------
# LOAD AND SAVE
# --------------------------------------------------

def load_entrances():
    if not ENTRANCES_FILE.exists():
        return {}

    try:
        with open(ENTRANCES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_entrances(data):
    with open(ENTRANCES_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Campus Entrance Marker",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Campus Building Entrance Marker")

st.write(
    "Select a location, zoom into the satellite map, "
    "and click on its actual pedestrian entrance."
)

st.info(
    "Select the correct building before marking its entrances. "
    "Each entrance will be saved under that building."
)


# --------------------------------------------------
# DELETE ALL ENTRANCES
# --------------------------------------------------

st.subheader("Manage saved entrances")

entrances = load_entrances()

total_entrances = sum(
    len(items) for items in entrances.values()
)

st.write(f"Total saved entrances: **{total_entrances}**")

if "confirm_delete_all" not in st.session_state:
    st.session_state.confirm_delete_all = False

if st.button(
    "🗑️ Delete All Saved Entrances",
    disabled=(total_entrances == 0)
):
    st.session_state.confirm_delete_all = True

if st.session_state.confirm_delete_all:

    st.warning(
        "Are you sure? This will permanently delete all saved entrances."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, delete everything", type="primary"):
            save_entrances({})
            st.session_state.confirm_delete_all = False
            st.session_state.pop("pending_entrance", None)
            st.success("All saved entrances have been deleted.")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.session_state.confirm_delete_all = False
            st.rerun()


# --------------------------------------------------
# SELECT BUILDING
# --------------------------------------------------

st.divider()

selected_location = st.selectbox(
    "Select a building or campus location",
    list(campus_coordinates.keys())
)

st.subheader(f"Mark entrances: {selected_location}")


# --------------------------------------------------
# MAP
# --------------------------------------------------

reference_coordinates = campus_coordinates[selected_location]

campus_map = folium.Map(
    location=reference_coordinates,
    zoom_start=19,
    tiles=None,
    control_scale=True
)

folium.TileLayer(
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/rest/"
        "services/World_Imagery/MapServer/tile/"
        "{z}/{y}/{x}"
    ),
    attr="Esri World Imagery",
    name="Satellite View"
).add_to(campus_map)

folium.TileLayer(
    tiles="OpenStreetMap",
    name="Street Map"
).add_to(campus_map)


# Approximate location markers

for name, coordinates in campus_coordinates.items():

    folium.CircleMarker(
        location=coordinates,
        radius=5,
        color="yellow",
        fill=True,
        fill_color="yellow",
        fill_opacity=0.8,
        tooltip=f"Approximate location: {name}"
    ).add_to(campus_map)


# Saved entrance markers

entrances = load_entrances()

for name, entrance_list in entrances.items():

    for entrance in entrance_list:

        folium.Marker(
            location=(entrance["lat"], entrance["lon"]),
            tooltip=f"{name} - {entrance['label']}",
            icon=folium.Icon(
                color="green",
                icon="map-marker",
                prefix="fa"
            )
        ).add_to(campus_map)


# Selected building reference marker

folium.Marker(
    location=reference_coordinates,
    tooltip=f"Approximate location: {selected_location}",
    icon=folium.Icon(
        color="orange",
        icon="building",
        prefix="fa"
    )
).add_to(campus_map)

folium.LayerControl().add_to(campus_map)

st.caption(
    "Yellow = Approximate locations | "
    "Green = Saved entrances | Orange = Selected location"
)


# --------------------------------------------------
# CAPTURE MAP CLICK
# --------------------------------------------------

map_result = st_folium(
    campus_map,
    width=None,
    height=650,
    returned_objects=["last_clicked"],
    key=f"entrance_map_{selected_location}"
)

if map_result and map_result.get("last_clicked"):

    clicked = map_result["last_clicked"]

    st.session_state["pending_entrance"] = {
        "location": selected_location,
        "lat": clicked["lat"],
        "lon": clicked["lng"]
    }


# --------------------------------------------------
# SAVE SELECTED ENTRANCE
# --------------------------------------------------

pending = st.session_state.get("pending_entrance")

if pending and pending["location"] == selected_location:

    st.divider()
    st.subheader("Selected entrance")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Latitude", f"{pending['lat']:.8f}")

    with col2:
        st.metric("Longitude", f"{pending['lon']:.8f}")

    current_entrances = load_entrances()

    saved_count = len(
        current_entrances.get(selected_location, [])
    )

    entrance_label = st.text_input(
        "Entrance name",
        value=f"Entrance {saved_count + 1}",
        key=f"entrance_label_{selected_location}_{saved_count}"
    )

    if st.button("Save this entrance", type="primary"):

        if not entrance_label.strip():
            st.error("Please enter an entrance name.")

        else:

            current_entrances.setdefault(
                selected_location, []
            )

            duplicate = any(
                abs(item["lat"] - pending["lat"]) < 0.00001
                and abs(item["lon"] - pending["lon"]) < 0.00001
                for item in current_entrances[selected_location]
            )

            if duplicate:
                st.warning("This entrance is already saved.")

            else:

                current_entrances[selected_location].append({
                    "label": entrance_label.strip(),
                    "lat": pending["lat"],
                    "lon": pending["lon"]
                })

                save_entrances(current_entrances)

                st.session_state.pop("pending_entrance", None)

                st.success("Entrance saved successfully!")
                st.rerun()


# --------------------------------------------------
# VIEW AND DELETE INDIVIDUAL ENTRANCES
# --------------------------------------------------

st.divider()
st.subheader("Saved entrances for selected location")

current_entrances = load_entrances()

location_entrances = current_entrances.get(
    selected_location, []
)

if location_entrances:

    for index, entrance in enumerate(location_entrances):

        st.write(
            f"**{entrance['label']}** — "
            f"{entrance['lat']:.8f}, {entrance['lon']:.8f}"
        )

        if st.button(
            f"Delete {entrance['label']}",
            key=f"delete_{selected_location}_{index}"
        ):

            current_entrances[selected_location].pop(index)

            if not current_entrances[selected_location]:
                del current_entrances[selected_location]

            save_entrances(current_entrances)

            st.success("Entrance deleted.")
            st.rerun()

else:
    st.caption("No entrances saved for this location.")

total_entrances = sum(
    len(items) for items in load_entrances().values()
)

st.caption(f"Total saved entrances: {total_entrances}")
