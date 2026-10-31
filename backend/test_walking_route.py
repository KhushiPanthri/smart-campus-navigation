
import requests

# Main Gate coordinates
start_lat, start_lon = 30.26861184622332, 77.99477040767671

# Admin Block coordinates
end_lat, end_lon = 30.267263605839172, 77.99527466297151

url = (
    f"https://routing.openstreetmap.de/routed-foot/route/v1/driving/"
    f"{start_lon},{start_lat};{end_lon},{end_lat}"
)

params = {
    "overview": "full",
    "geometries": "geojson"
}

try:
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    result = response.json()

    if result.get("code") == "Ok":
        coordinates = result["routes"][0]["geometry"]["coordinates"]

        print("Walking route found!")
        print("Number of route points:", len(coordinates))
        print("First point:", coordinates[0])
        print("Last point:", coordinates[-1])
    else:
        print("No walking route found:", result)

except requests.RequestException as error:
    print("Request failed:", error)
