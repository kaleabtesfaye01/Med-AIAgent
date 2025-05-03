import os
from functools import lru_cache
from typing import Dict, List, Any
import googlemaps
from geopy.geocoders import Nominatim

# Load API key from environment
GOOGLE_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
if not GOOGLE_KEY:
    raise RuntimeError("Missing GOOGLE_PLACES_API_KEY in environment")

gmaps = googlemaps.Client(key=GOOGLE_KEY)
geolocator = Nominatim(user_agent="treatment-agent")

@lru_cache(maxsize=128)
def geocode(address: str) -> Dict[str, float]:
    """
    Convert an address string into latitude and longitude.
    Results are cached to avoid redundant lookups.
    """
    loc = geolocator.geocode(address)
    if not loc:
        raise ValueError(f"Could not geocode address: {address}")
    return {"lat": loc.latitude, "lng": loc.longitude}

@lru_cache(maxsize=128)
def find_nearby_hospitals(
    lat: float,
    lng: float,
    k: int = 3
) -> List[Dict[str, Any]]:
    """
    Use Google Places Nearby Search to find up to `k` hospitals by distance.
    Caches results by coordinates.
    """
    try:
        places = gmaps.places_nearby(
            location=(lat, lng),
            rank_by="distance",
            type="hospital"
        ).get("results", [])
    except googlemaps.exceptions.ApiError as e:
        raise RuntimeError(f"Google Places API error: {e}")

    hospitals: List[Dict[str, Any]] = []
    for p in places[:k]:
        loc = p.get("geometry", {}).get("location", {})
        hospitals.append({
            "name": p.get("name"),
            "address": p.get("vicinity"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "rating": p.get("rating")
        })
    return hospitals