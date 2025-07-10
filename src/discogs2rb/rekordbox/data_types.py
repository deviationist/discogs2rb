from typing import NamedTuple, Optional


class Artist(NamedTuple):
    id: int
    name: str


class Album(NamedTuple):
    id: int
    name: str


class Track(NamedTuple):
    id: int
    title: str
    release_year: int
    release_date: str
    artist: Optional[Artist]
    album: Optional[Album]
    album_artist: Optional[Artist]
