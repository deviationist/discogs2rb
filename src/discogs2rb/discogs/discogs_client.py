import requests
import time
import re
from ..config import get_discogs_token
from typing import Optional, List, Any
from ..config import get_various_artist_name
from ..utils.logger import logger
from .data_types import ResolvedRelease

# Constants
DISCOGS_BASE_URL = "https://api.discogs.com"
RATE_LIMIT = 60  # Max 60 requests per minute
RATE_LIMIT_INTERVAL = 60  # In seconds
USER_AGENT = "discogs2rb/1.0"

# Global rate limit state
RATE_LIMIT_BUFFER = 2  # How many requests to leave unused as buffer


def rate_limited_request(url: str, params: dict = {}) -> Optional[dict]:
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Discogs token={get_discogs_token()}",
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 429:
            logger.debug(
                "[Rate Limit Hit] Received 429 Too Many Requests. Sleeping 60 seconds..."
            )
            time.sleep(60)
            return rate_limited_request(url, params)

        # Check rate limit headers
        remaining = int(response.headers.get("X-Discogs-Ratelimit-Remaining", "60"))
        used = int(response.headers.get("X-Discogs-Ratelimit-Used", "0"))
        limit = int(response.headers.get("X-Discogs-Ratelimit", "60"))

        logger.debug(
            f"[Rate Limit] Used: {used}, Remaining: {remaining}, Total Limit: {limit}"
        )

        if remaining <= RATE_LIMIT_BUFFER:
            print("[Throttling] Near rate limit. Sleeping 5 seconds...")
            time.sleep(5)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[Error] Status Code: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"[Exception] {e}")
        return None


def is_various(artists) -> bool:
    if artists:
        for artist in artists:
            if artist.get("name") == "Various":
                return True
    return False


def get_primary_image_url(images) -> str | None:
    logger.debug("Looking for primary image")
    if images:
        for image in images:
            if image.get("type") == "primary":
                logger.debug("Found primary image")
                return image.get("resource_url")
    logger.debug("Did not find primary image")
    return None


def get_artist_names(artists) -> str | None:
    if artists:
        artist_names = []
        for artist in artists:
            artist_name = artist.get("name")
            if artist_name:
                artist_names.append(artist_name)
        artist_names = list(set(artist_names))
        return ", ".join(artist_names)
    return None


def get_release_date(release_data: Any) -> str:
    release_date = release_data.get("released")
    if isinstance(release_date, str):
        return re.sub("-00$", "", release_date)
    return ""


def search_release_metadata(
    track: str, artist: str, allow_multiple_hits: bool = True
) -> Optional[List[ResolvedRelease]]:
    """
    Search for a release by track and artist name.
    Returns metadata like title, artist, year, and release date.
    """
    params = {"q": f"{artist} {track}", "type": "release", "per_page": 1, "page": 1}

    logger.debug(f'Searching for track "{track}" by "{artist}"')

    data = rate_limited_request(f"{DISCOGS_BASE_URL}/database/search", params)
    if not data or "results" not in data or len(data["results"]) == 0:
        logger.debug("[No Results] No matching release found.")
        return None

    raw_releases = data["results"]
    if not raw_releases or len(raw_releases) == 0:
        return None

    if not allow_multiple_hits:
        raw_releases = raw_releases[:1]

    logger.debug(f"Found {len(raw_releases)} hits, proceeding to parse.")
    releases = []
    for release in raw_releases:
        release_id = release.get("id")
        logger.debug(f'Resolving release by ID "{release_id}"')
        release_data = rate_limited_request(f"{DISCOGS_BASE_URL}/releases/{release_id}")
        artists = release_data.get("artists") if release_data else ""
        artist_names = get_artist_names(artists)
        images = release_data.get("images") if release_data else ""
        image = get_primary_image_url(images)

        various_artist_name = get_various_artist_name()
        if artist_names == "Various":
            artist_names = various_artist_name
        release_date = get_release_date(release_data)
        releases.append(
            ResolvedRelease(
                album_title=release_data.get("title") if release_data else "",
                album_artists=artist_names,
                release_year=release_data.get("year") if release_data else "",
                release_date=release_date,
                release_url=release_data.get("uri") if release_data else "",
                image=image if image else release.get("cover_image"),
                is_various=is_various(artists),
            )
        )
    if len(releases) > 0:
        return releases
    return None
