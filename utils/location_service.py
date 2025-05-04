import os
from functools import lru_cache
from typing import Dict, List, Optional
import googlemaps
from geopy.geocoders import Nominatim

# Load API key from environment
GOOGLE_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
if not GOOGLE_KEY:
    raise RuntimeError("Missing GOOGLE_PLACES_API_KEY in environment")

gmaps = googlemaps.Client(key=GOOGLE_KEY)
geolocator = Nominatim(user_agent="treatment-agent")

def build_full_address(
    address1: str,
    address2: Optional[str],
    city: str,
    state: str,
    country: str,
    zip_code: Optional[str] = None,
    postal_code: Optional[str] = None
) -> str:
    """
    Combine address components into a full address string.
    """
    parts = [address1]
    if address2:
        parts.append(address2)
    parts.extend([city, state, country])
    if zip_code:
        parts.append(zip_code)
    if postal_code:
        parts.append(postal_code)
    return ", ".join(parts)

@lru_cache(maxsize=128)
def geocode(address: str) -> Dict[str, float]:
    """
    Convert an address string into latitude and longitude.
    First attempts with geopy; if that fails, falls back to Google Maps Geocoding API.
    Results are cached to avoid redundant lookups.
    """
    # Try with Nominatim
    loc = geolocator.geocode(address)
    if loc:
        return {"lat": loc.latitude, "lng": loc.longitude}
    # Fallback to Google Maps Geocode
    try:
        results = gmaps.geocode(address)
        if results:
            geom = results[0].get("geometry", {}).get("location", {})
            return {"lat": geom.get("lat"), "lng": geom.get("lng")}
    except Exception:
        pass
    raise ValueError(f"Could not geocode address: {address}")

@lru_cache(maxsize=128)
def geocode_components(
    address1: str,
    address2: Optional[str],
    city: str,
    state: str,
    country: str,
    zip_code: Optional[str] = None,
    postal_code: Optional[str] = None
) -> Dict[str, float]:
    """
    Build a full address from components and geocode it.
    """
    full_address = build_full_address(
        address1, address2, city, state, country, zip_code, postal_code
    )
    return geocode(full_address)

@lru_cache(maxsize=128)
def find_nearby_hospitals(
    lat: float,
    lng: float,
    k: int = 3
) -> List[Dict[str, any]]:
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

    hospitals: List[Dict[str, any]] = []
    for p in places[:k]:
        loc = p.get("geometry", {}).get("location", {})
        hospitals.append({
            "name": p.get("name"),
            "address": p.get("vicinity"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "rating": p.get("rating"),
        })
    return hospitals