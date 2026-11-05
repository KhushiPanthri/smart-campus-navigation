
import json
import math
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import Fullscreen, LocateControl, MeasureControl

from campus_coordinates import campus_coordinates


VALHALLA_URL = "https://valhalla1.openstreetmap.de/route"

BACKEND_DIR = Path(__file__).resolve().parent
ENTRANCES_FILE = BACKEND_DIR / "entrances.json"

MAX_CONNECTION_GAP_METERS = 50
REQUEST_TIMEOUT = 25
MAX_WORKERS = 4


# --------------------------------------------------
# LOAD ENTRANCE DATA
# --------------------------------------------------

def load_entrances():

    try:
        with open(ENTRANCES_FILE, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

    except FileNotFoundError:
        st.error("entrances.json was not found in the backend folder.")
        return {}

    except json.JSONDecodeError:
        st.error("entrances.json contains invalid JSON.")
        return {}

    entrances = {}

    for location_name, points in raw_data.items():

        valid_points = []

        if not isinstance(points, list):
            continue

        for point in points:

            try:
                lat = float(point["lat"])
                lon = float(point["lon"])

                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue

                valid_points.append({
                    "label": point.get("label", "Entrance"),
                    "lat": lat,
                    "lon": lon
                })

            except (KeyError, TypeError, ValueError):
                continue

        if valid_points:
            entrances[location_name] = valid_points

    return entrances


# --------------------------------------------------
# GET AVAILABLE POINTS FOR A LOCATION
# --------------------------------------------------

def get_location_points(name, entrances):

    if name in entrances and entrances[name]:
        return entrances[name]

    # Use old coordinates only as a fallback.

    if name in campus_coordinates:

        lat, lon = campus_coordinates[name]

        return [{
            "label": "Default location",
            "lat": lat,
            "lon": lon
        }]

    return []


# --------------------------------------------------
# DISTANCE BETWEEN TWO COORDINATES
# --------------------------------------------------

def calculate_distance(point1, point2):

    earth_radius = 6371000

    lat1 = math.radians(point1[0])
    lon1 = math.radians(point1[1])

    lat2 = math.radians(point2[0])
    lon2 = math.radians(point2[1])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    return earth_radius * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


# --------------------------------------------------
# POLYLINE6 DECODER
# --------------------------------------------------

def decode_polyline(encoded, precision=6):

    coordinates = []

    index = 0
    latitude = 0
    longitude = 0

    factor = 10 ** precision

    while index < len(encoded):

        values = []

        for _ in range(2):

            result = 0
            shift = 0

            while True:

                if index >= len(encoded):
                    raise ValueError("Incomplete polyline data")

                byte = ord(encoded[index]) - 63
                index += 1

                if byte < 0 or byte > 63:
                    raise ValueError("Invalid polyline character")

                result |= (byte & 0x1F) << shift
                shift += 5

                if byte < 0x20:
                    break

                if shift > 60:
                    raise ValueError("Invalid polyline encoding")

            delta = (
                ~(result >> 1)
                if result & 1
                else result >> 1
            )

            values.append(delta)

        latitude += values[0]
        longitude += values[1]

        coordinates.append(
            (latitude / factor, longitude / factor)
        )

    return coordinates


# --------------------------------------------------
# REQUEST ONE WALKING ROUTE FROM VALHALLA
# --------------------------------------------------

def request_walking_route(start_point, end_point):

    payload = {
        "locations": [
            {
                "lat": start_point["lat"],
                "lon": start_point["lon"]
            },
            {
                "lat": end_point["lat"],
                "lon": end_point["lon"]
            }
        ],
        "costing": "pedestrian",
        "units": "kilometers",
        "shape_format": "polyline6"
    }

    request = urllib.request.Request(
        VALHALLA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        if "error" in result:
            return None

        legs = result.get("trip", {}).get("legs", [])

        if len(legs) != 1:
            return None

        leg = legs[0]

        encoded_shape = leg.get("shape")

        if not encoded_shape:
            return None

        coordinates = decode_polyline(encoded_shape)

        if len(coordinates) < 2:
            return None

        for lat, lon in coordinates:

            if not (
                -90 <= lat <= 90
                and -180 <= lon <= 180
            ):
                return None

        # Prefer Valhalla's actual walking distance.

        distance = leg.get("summary", {}).get("length")

        if distance is None:

            distance = sum(
                calculate_distance(
                    coordinates[i],
                    coordinates[i + 1]
                )
                for i in range(len(coordinates) - 1)
            ) / 1000

        return {
            "coordinates": coordinates,
            "distance": float(distance)
        }

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        ValueError,
        KeyError,
        TypeError,
        IndexError
    ):
        return None


# --------------------------------------------------
# FIND THE BEST ENTRANCE COMBINATION FOR THE ROUTE
# --------------------------------------------------

def get_walking_paths(route_locations, entrances):

    if len(route_locations) < 2:
        return None, None, "At least two locations are required."

    candidates = []

    for name in route_locations:

        points = get_location_points(name, entrances)

        if not points:
            return None, None, f"No coordinates found for {name}."

        candidates.append(points)

    # Store every possible route between consecutive locations.

    route_options = {}

    tasks = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        for edge_index in range(len(route_locations) - 1):

            start_points = candidates[edge_index]
            end_points = candidates[edge_index + 1]

            for start_index, start_point in enumerate(start_points):

                for end_index, end_point in enumerate(end_points):

                    future = executor.submit(
                        request_walking_route,
                        start_point,
                        end_point
                    )

                    tasks[future] = (
                        edge_index,
                        start_index,
                        end_index
                    )

        for future in as_completed(tasks):

            key = tasks[future]

            try:
                result = future.result()

                if result is not None:
                    route_options[key] = result

            except Exception:
                continue

    # --------------------------------------------------
    # DYNAMIC PROGRAMMING
    # Choose one entrance per location so consecutive
    # route segments use the same intermediate entrance.
    # --------------------------------------------------

    costs = [
        [float("inf")] * len(points)
        for points in candidates
    ]

    predecessors = [
        [None] * len(points)
        for points in candidates
    ]

    # Every entrance at the starting location is possible.

    costs[0] = [0] * len(candidates[0])

    for edge_index in range(len(route_locations) - 1):

        next_costs = [float("inf")] * len(
            candidates[edge_index + 1]
        )

        for start_index in range(len(candidates[edge_index])):

            if costs[edge_index][start_index] == float("inf"):
                continue

            for end_index in range(
                len(candidates[edge_index + 1])
            ):

                key = (
                    edge_index,
                    start_index,
                    end_index
                )

                option = route_options.get(key)

                if option is None:
                    continue

                new_cost = (
                    costs[edge_index][start_index]
                    + option["distance"]
                )

                if new_cost < next_costs[end_index]:

                    next_costs[end_index] = new_cost

                    predecessors[edge_index + 1][end_index] = (
                        start_index
                    )

        costs[edge_index + 1] = next_costs

        if all(value == float("inf") for value in next_costs):

            return (
                None,
                None,
                f"No continuous walking route could be calculated "
                f"between {route_locations[edge_index]} and "
                f"{route_locations[edge_index + 1]}."
            )

    # --------------------------------------------------
    # BACKTRACK TO FIND THE SELECTED ENTRANCES
    # --------------------------------------------------

    final_index = min(
        range(len(costs[-1])),
        key=lambda index: costs[-1][index]
    )

    selected_indices = [None] * len(route_locations)

    selected_indices[-1] = final_index

    for index in range(len(route_locations) - 1, 0, -1):

        previous_index = predecessors[index][
            selected_indices[index]
        ]

        if previous_index is None:
            return None, None, "Unable to reconstruct the walking route."

        selected_indices[index - 1] = previous_index

    selected_points = [
        candidates[index][selected_indices[index]]
        for index in range(len(route_locations))
    ]

    # --------------------------------------------------
    # COLLECT THE SELECTED ROUTE SEGMENTS
    # --------------------------------------------------

    route_segments = []

    for edge_index in range(len(route_locations) - 1):

        key = (
            edge_index,
            selected_indices[edge_index],
            selected_indices[edge_index + 1]
        )

        option = route_options.get(key)

        if option is None:
            return None, None, "A selected walking segment is missing."

        route_segments.append(option["coordinates"])

    # --------------------------------------------------
    # CHECK CONNECTIONS BETWEEN ROUTE SEGMENTS
    # --------------------------------------------------

    for index in range(len(route_segments) - 1):

        previous_end = route_segments[index][-1]
        next_start = route_segments[index + 1][0]

        gap = calculate_distance(
            previous_end,
            next_start
        )

        if gap > MAX_CONNECTION_GAP_METERS:

            return (
                None,
                None,
                f"Walking route segments are disconnected near "
                f"{route_locations[index + 1]}. "
                f"Connection gap: {gap:.1f} metres."
            )

    return route_segments, selected_points, None


# --------------------------------------------------
# FACILITY MARKER STYLING
# --------------------------------------------------

def get_marker_style(name):

    name_lower = name.lower()

    if "gate" in name_lower:
        return "green", "sign-in-alt", "Gate"

    if "library" in name_lower or "lab" in name_lower:
        return "blue", "book", "Academic Facility"

    if (
        "cafe" in name_lower
        or "canteen" in name_lower
        or "tuckshop" in name_lower
    ):
        return "orange", "cutlery", "Food Facility"

    if "ground" in name_lower or "court" in name_lower:
        return "purple", "futbol", "Sports Facility"

    return "cadetblue", "building", "Campus Building"


# --------------------------------------------------
# MAIN CAMPUS MAP
# --------------------------------------------------

def display_campus_map(route=None):

    entrances = load_entrances()

    main_gate_points = get_location_points(
        "Main Gate",
        entrances
    )

    if not main_gate_points:
        st.error("Main Gate coordinates are missing.")
        return

    main_gate = (
        main_gate_points[0]["lat"],
        main_gate_points[0]["lon"]
    )

    campus_map = folium.Map(
        location=main_gate,
        zoom_start=18,
        tiles=None,
        control_scale=True,
        prefer_canvas=True
    )

    # --------------------------------------------------
    # MAP LAYERS
    # --------------------------------------------------

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Street Map",
        control=True
    ).add_to(campus_map)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/"
            "services/World_Imagery/MapServer/tile/"
            "{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="Satellite View",
        overlay=False,
        control=True
    ).add_to(campus_map)

    # --------------------------------------------------
    # MAP CONTROLS
    # --------------------------------------------------

    Fullscreen(
        position="topright",
        title="Open Fullscreen",
        title_cancel="Exit Fullscreen"
    ).add_to(campus_map)

    LocateControl(
        auto_start=False,
        flyTo=True,
        keepCurrentZoomLevel=False,
        showPopup=True
    ).add_to(campus_map)

    MeasureControl(
        position="bottomleft",
        primary_length_unit="meters",
        secondary_length_unit="kilometers"
    ).add_to(campus_map)

    # --------------------------------------------------
    # CAMPUS ENTRANCE MARKERS
    # --------------------------------------------------

    all_locations = set(campus_coordinates.keys())
    all_locations.update(entrances.keys())

    for name in sorted(all_locations):

        points = get_location_points(name, entrances)

        color, icon, category = get_marker_style(name)

        for point in points:

            entrance_label = point["label"]

            folium.Marker(
                location=(point["lat"], point["lon"]),
                tooltip=f"{name} - {entrance_label}",
                popup=folium.Popup(
                    f"<b>{name}</b><br>"
                    f"{entrance_label}<br>"
                    f"{category}",
                    max_width=220
                ),
                icon=folium.Icon(
                    color=color,
                    icon=icon,
                    prefix="fa"
                )
            ).add_to(campus_map)

    # --------------------------------------------------
    # WALKING ROUTE DISPLAY
    # --------------------------------------------------

    if route and len(route) >= 2:

        missing_locations = [
            name
            for name in route
            if not get_location_points(name, entrances)
        ]

        if missing_locations:

            st.error(
                "Coordinates missing for: "
                + ", ".join(missing_locations)
            )

        else:

            (
                route_segments,
                selected_points,
                route_error
            ) = get_walking_paths(route, entrances)

            if route_error:

                st.error(
                    f"Walking route unavailable: {route_error}"
                )

                st.warning(
                    "No straight-line fallback is displayed. "
                    "The map will not show an invented route."
                )

            else:

                all_route_coordinates = []

                # Draw every selected walking segment.

                for index, segment in enumerate(route_segments):

                    folium.PolyLine(
                        locations=segment,
                        color="#1677FF",
                        weight=7,
                        opacity=0.9,
                        tooltip=(
                            f"{route[index]} → {route[index + 1]}"
                        )
                    ).add_to(campus_map)

                    all_route_coordinates.extend(segment)

                # --------------------------------------------------
                # START MARKER
                # --------------------------------------------------

                start_point = selected_points[0]

                folium.Marker(
                    location=(
                        start_point["lat"],
                        start_point["lon"]
                    ),
                    tooltip="Starting Location",
                    popup=f"Start: {route[0]}",
                    icon=folium.Icon(
                        color="green",
                        icon="play",
                        prefix="fa"
                    )
                ).add_to(campus_map)

                # --------------------------------------------------
                # DESTINATION MARKER
                # --------------------------------------------------

                end_point = selected_points[-1]

                folium.Marker(
                    location=(
                        end_point["lat"],
                        end_point["lon"]
                    ),
                    tooltip="Destination",
                    popup=f"Destination: {route[-1]}",
                    icon=folium.Icon(
                        color="red",
                        icon="flag",
                        prefix="fa"
                    )
                ).add_to(campus_map)

                # --------------------------------------------------
                # FIT MAP TO ROUTE
                # --------------------------------------------------

                campus_map.fit_bounds(
                    all_route_coordinates,
                    padding=(35, 35)
                )

    # --------------------------------------------------
    # LAYER CONTROL
    # --------------------------------------------------

    folium.LayerControl(
        position="topright",
        collapsed=True
    ).add_to(campus_map)

    # --------------------------------------------------
    # DISPLAY MAP
    # --------------------------------------------------

    st_folium(
        campus_map,
        width=1100,
        height=680,
        returned_objects=[],
        key="smart_campus_navigation_map"
    )
