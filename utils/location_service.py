from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List, Dict

geolocator = Nominatim(user_agent="my-app")

def geocode(address: str) -> Dict[str, float]:
    loc = geolocator.geocode(address)
    return {"lat": loc.latitude, "lng": loc.longitude}

# For demo, a hard-coded list of facilities; in prod, replace with real API/DB
FACILITIES = [
    {"name": "St. Elizabeth Hospital", "lat": 39.0495, "lng": -84.5120},
    {"name": "TeleHealth Clinic",    "lat": 39.1000, "lng": -84.5000},
    # …etc…
]

def nearest_facilities(user_loc: Dict[str, float], k: int = 3) -> List[Dict]:
    dists = []
    for f in FACILITIES:
        dist = geodesic((user_loc["lat"], user_loc["lng"]), (f["lat"], f["lng"])).miles
        dists.append((dist, f))
    return [f for _, f in sorted(dists)[:k]]