
import folium
import streamlit as st
from streamlit_folium import st_folium

from campus_coordinates import campus_coordinates


def display_campus_map(route=None):

    campus_map = folium.Map(
        location=campus_coordinates["Main Gate"],
        zoom_start=18,
        tiles="OpenStreetMap"
    )

    # Display all campus locations
    for name, coords in campus_coordinates.items():
        folium.Marker(
            location=coords,
            popup=name,
            tooltip=name
        ).add_to(campus_map)

    # Display the route calculated by Dijkstra
    if route and len(route) >= 2:

        route_coordinates = [
            campus_coordinates[location]
            for location in route
            if location in campus_coordinates
        ]

        if len(route_coordinates) >= 2:

            folium.PolyLine(
                locations=route_coordinates,
                color="blue",
                weight=6,
                opacity=0.8,
                tooltip="Shortest Route (Dijkstra)"
            ).add_to(campus_map)

            # Mark starting location
            folium.Marker(
                route_coordinates[0],
                popup="Start",
                icon=folium.Icon(color="green", icon="play")
            ).add_to(campus_map)

            # Mark destination
            folium.Marker(
                route_coordinates[-1],
                popup="Destination",
                icon=folium.Icon(color="red", icon="flag")
            ).add_to(campus_map)

            campus_map.fit_bounds(route_coordinates)

    st_folium(campus_map, width=750, height=550)
