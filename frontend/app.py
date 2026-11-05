
import streamlit as st
import sys
import os
import html


# --------------------------------------------------
# BACKEND IMPORTS
# --------------------------------------------------

BACKEND_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "backend"
    )
)

if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)


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
    layout="wide",
    initial_sidebar_state="collapsed"
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

    /* Main page */

    .stApp {
        background-color: #f3f6fb;
    }

    .block-container {
        max-width: 100%;
        padding: 1rem 1.5rem 2rem 1.5rem;
    }

    /* Navigation header */

    .nav-header {
        background: linear-gradient(
            110deg,
            #102b50,
            #174b7a
        );

        padding: 18px 25px;
        border-radius: 14px;
        color: white;
        margin-bottom: 18px;

        display: flex;
        justify-content: space-between;
        align-items: center;

        box-shadow: 0 5px 18px rgba(15, 40, 75, 0.16);
    }

    .nav-title {
        font-size: 27px;
        font-weight: 750;
        letter-spacing: 0.2px;
    }

    .nav-subtitle {
        font-size: 13px;
        color: #d6e4f5;
        margin-top: 3px;
    }

    .nav-status {
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.2);
        padding: 8px 13px;
        border-radius: 20px;
        font-size: 12px;
    }

    /* Route panel */

    .panel-heading {
        color: #183657;
        font-size: 21px;
        font-weight: 750;
        margin-bottom: 4px;
    }

    .panel-caption {
        color: #718096;
        font-size: 13px;
        margin-bottom: 15px;
    }

    div.st-key-route_panel {
        background: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e0e7f0;
        box-shadow: 0 4px 15px rgba(25, 50, 80, 0.07);
    }

    /* Input fields */

    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 43px;
    }

    /* Map heading */

    .map-heading {
        color: #183657;
        font-size: 20px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .map-caption {
        color: #718096;
        font-size: 13px;
        margin-bottom: 10px;
    }

    /* Route result */

    .result-card {
        background: white;
        border: 1px solid #e0e7f0;
        border-radius: 12px;
        padding: 15px;
        margin-top: 14px;
    }

    .result-label {
        color: #718096;
        font-size: 12px;
        margin-bottom: 5px;
    }

    .result-value {
        color: #183657;
        font-size: 24px;
        font-weight: 750;
    }

    .route-stop {
        background: #f4f7fb;
        border-left: 3px solid #2475c5;
        padding: 9px 12px;
        margin: 7px 0;
        border-radius: 5px;
        color: #243b53;
        font-size: 14px;
    }

    /* Section headings */

    h2, h3 {
        color: #183657;
    }

    /* Footer */

    .footer {
        color: #7b8794;
        text-align: center;
        font-size: 12px;
        padding: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# NAVIGATION HEADER
# --------------------------------------------------

# --------------------------------------------------
# NAVIGATION HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="nav-header">
        <div>
            <div class="nav-title">
                🏫 Smart Campus Navigation
            </div>
            <div class="nav-subtitle">
                Explore the campus. Find your way.
            </div>
        </div>
        <div class="nav-status">
            ● Campus Map
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# MAIN LAYOUT
# Map gets most of the available width.
# --------------------------------------------------

panel_col, map_col = st.columns(
    [1, 3],
    gap="large"
)


location_names = list(locations.keys())


# --------------------------------------------------
# ROUTE SEARCH PANEL
# --------------------------------------------------

with panel_col:

    with st.container(key="route_panel"):

        st.markdown(
            '<div class="panel-heading">Plan Your Route</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-caption">Choose starting point and destination.</div>',
            unsafe_allow_html=True
        )

        start = st.selectbox(
            "Starting location",
            location_names,
            key="start_location"
        )

        destination = st.selectbox(
            "Destination",
            location_names,
            index=1 if len(location_names) > 1 else 0,
            key="destination_location"
        )

        find_route = st.button(
            "🔍 Find Walking Route",
            use_container_width=True,
            type="primary"
        )

        if find_route:

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

        # ------------------------------------------
        # ROUTE SEARCH
        # ------------------------------------------

        st.divider()

        st.markdown("**Quick Location Search**")
            
        quick_location = st.selectbox(

            "Select a campus location",
            ["Choose a location"] + location_names,
            key="quick_location",
            label_visibility="collapsed"
        )
        
        if quick_location != "Choose a location":
            st.info(f"📍 Selected: {quick_location}")
            location_info = locations[quick_location]
            st.write(f"**Type:** {location_info['type']}")
            st.write(location_info["description"])

        # ------------------------------------------
        # ROUTE ERRORS
        # ------------------------------------------

        if st.session_state.route_error:

            st.error(
                st.session_state.route_error
            )

        # ------------------------------------------
        # ROUTE SUMMARY
        # ------------------------------------------

        if st.session_state.route is not None:

            st.divider()

            st.success("Shortest route found!")

            st.markdown("**Your Route**")

            for index, location in enumerate(
                st.session_state.route
            ):

                safe_location = html.escape(location)

                if index == 0:

                    st.markdown(
                        f'<div class="route-stop">🟢 <b>Start:</b> {safe_location}</div>',
                        unsafe_allow_html=True
                    )

                elif index == len(st.session_state.route) - 1:

                    st.markdown(
                        f'<div class="route-stop">🔴 <b>Destination:</b> {safe_location}</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f'<div class="route-stop">➡️ {safe_location}</div>',
                        unsafe_allow_html=True
                    )

            st.metric(
                "Total Dijkstra Distance",
                f"{st.session_state.distance} m"
            )

        else:

            st.divider()

            st.caption(
                " "
            )


# --------------------------------------------------
# CAMPUS MAP
# Visible even before route selection.
# --------------------------------------------------

with map_col:

    st.markdown(
        '<div class="map-heading">🗺️ Campus Map</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="map-caption">Explore campus locations and view your calculated walking route.</div>',
        unsafe_allow_html=True
    )

    current_route = st.session_state.route

    display_campus_map(current_route)


# --------------------------------------------------
# LOCATION INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("📍 Campus Location Details")

selected_location = st.selectbox(
    "Select a campus location",
    location_names,
    key="location_information"
)

location_info = locations[selected_location]

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.markdown("**Location**")
    st.write(selected_location)

with info_col2:

    st.markdown("**Facility Type**")
    st.write(location_info["type"])

st.markdown("**Description**")
st.write(location_info["description"])


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Smart Campus Navigation System
        &nbsp;•&nbsp;
        Team Syntax Squad
    </div>
    """,
    unsafe_allow_html=True
)
