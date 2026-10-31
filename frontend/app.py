
import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from algorithms import find_shortest_route, search_locations
from data import locations
from graph import graph
from campus_map import display_campus_map


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Campus Navigation",
    page_icon="🏫",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "route" not in st.session_state:
    st.session_state.route = None

if "distance" not in st.session_state:
    st.session_state.distance = None

if "route_error" not in st.session_state:
    st.session_state.route_error = None


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .route-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    .route-step {
        font-size: 18px;
        font-weight: 500;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🏫 Smart Campus Navigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find the shortest route between campus locations</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🔎 Campus Search")

search_term = st.sidebar.text_input(
    "Search for a location",
    placeholder="Example: Library"
)

if search_term:

    search_results = search_locations(
        locations.keys(),
        search_term
    )

    if search_results:

        st.sidebar.success(
            f"{len(search_results)} location(s) found"
        )

        for location in search_results:
            st.sidebar.write(f"📍 **{location}**")

    else:
        st.sidebar.warning("No matching location found.")


# --------------------------------------------------
# NAVIGATION SECTION
# --------------------------------------------------

st.subheader("📍 Find Your Route")

location_names = list(locations.keys())

col1, col2 = st.columns(2)

with col1:
    start = st.selectbox(
        "Starting Location",
        location_names
    )

with col2:
    destination = st.selectbox(
        "Destination",
        location_names,
        index=1 if len(location_names) > 1 else 0
    )


# --------------------------------------------------
# FIND ROUTE BUTTON
# --------------------------------------------------

if st.button(
    "🔍 Find Shortest Route",
    use_container_width=True
):

    # Clear previous result
    st.session_state.route = None
    st.session_state.distance = None
    st.session_state.route_error = None

    if start == destination:

        st.session_state.route_error = (
            "Starting location and destination cannot be the same."
        )

    else:

        route, distance = find_shortest_route(
            graph,
            start,
            destination
        )

        if route is None:

            st.session_state.route_error = distance

        else:

            st.session_state.route = route
            st.session_state.distance = distance


# --------------------------------------------------
# DISPLAY ROUTE RESULTS
# --------------------------------------------------

if st.session_state.route_error:

    st.warning(st.session_state.route_error)


elif st.session_state.route is not None:

    route = st.session_state.route
    distance = st.session_state.distance

    st.success("Shortest route found!")

    # ------------------------------------------
    # ROUTE DISPLAY
    # ------------------------------------------

    st.subheader("🛣️ Shortest Route")

    route_text = " → ".join(route)

    st.markdown(
        f"""
        <div class="route-box">
            <div class="route-step">
                {route_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------
    # DISTANCE
    # ------------------------------------------

    st.metric(
        label="📏 Total Distance",
        value=f"{distance} m"
    )

    # ------------------------------------------
    # STEP-BY-STEP ROUTE
    # ------------------------------------------

    st.subheader("📌 Step-by-Step Navigation")

    for i, location in enumerate(route):

        if i == 0:

            st.write(f"🟢 **Start:** {location}")

        elif i == len(route) - 1:

            st.write(f"🔴 **Destination:** {location}")

        else:

            st.write(f"➡️ {location}")

    # ------------------------------------------
    # CAMPUS MAP
    # ------------------------------------------

    st.divider()

    st.subheader("🗺️ Campus Route Map")

    st.write(
        "The map displays campus locations and "
        "highlights your calculated shortest route."
    )

    display_campus_map(route)


# --------------------------------------------------
# LOCATION INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("📖 Campus Location Information")

selected_location = st.selectbox(
    "Select a location to view details",
    location_names,
    key="location_information"
)

location_info = locations[selected_location]

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.write("### 📍 Location")
    st.write(selected_location)

with info_col2:

    st.write("### 🏷️ Type")
    st.write(location_info["type"])

st.write("### ℹ️ Description")

description = location_info["description"]

st.write(description)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Smart Campus Navigation System • Powered by "
    "Dijkstra's Shortest Path Algorithm"
)
