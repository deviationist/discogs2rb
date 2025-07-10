from typing import NamedTuple, Any


class ResolvedRelease(NamedTuple):
    album_title: Any
    album_artists: Any
    release_year: Any
    release_date: Any
    release_url: Any
    image: Any
    is_various: bool
