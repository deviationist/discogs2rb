from ..RekordboxDB import RekordboxDB
from ...utils.logger import logger
from ..data_types import Track, Artist, Album
from typing import Literal, List


def get_tracks_with_missing_album() -> List[Track] | Literal[False]:
    db = RekordboxDB()
    cursor = db.cursor

    try:
        query = """
        SELECT
            c.ID AS TrackID,
            c.Title AS TrackTitle,
            c.ReleaseYear AS TrackReleaseYear,
            c.ReleaseDate AS TrackReleaseDate,
            a.ID AS ArtistID,
            a.Name AS ArtistName,
            al.ID AS AlbumID,
            al.Name AS AlbumName,
            aa.ID AS AlbumArtistID,
            aa.Name AS AlbumArtistName
        FROM
            djmdContent AS c
        INNER JOIN djmdArtist AS a
            ON c.ArtistID = a.ID
        LEFT JOIN djmdAlbum AS al
            ON c.AlbumID = al.ID
        LEFT JOIN djmdArtist AS aa
            ON al.AlbumArtistID = aa.ID
        WHERE
            c.rb_local_deleted = 0
            AND c.rb_local_deleted = 0
            AND c.FolderPath NOT LIKE '%Memes%'
            AND (
                AlbumID IS NULL
                OR AlbumArtistID IS NULL
            )
"""
        cursor.execute(query)

        rows = cursor.fetchall()
        if rows:
            tracks = []

            for row in rows:
                # Convert row to dict for easier handling
                row_dict = dict(row)
                artist = None
                album = None
                album_artist = None

                if row_dict.get("ArtistID"):
                    artist = Artist(
                        id=int(row_dict["ArtistID"]),
                        name=row_dict["ArtistName"],
                    )

                if row_dict.get("AlbumID"):
                    album = Album(
                        id=int(row_dict["AlbumID"]),
                        name=row_dict["AlbumName"]
                    )

                if row_dict.get("AlbumArtistID"):
                    album_artist = Album(
                        id=int(row_dict["AlbumArtistID"]),
                        name=row_dict["AlbumArtistName"]
                    )

                # Provide None for artwork fields if they don't exist
                tracks.append(
                    Track(
                        id=int(row_dict["TrackID"]),
                        title=row_dict["TrackTitle"],
                        release_year=int(row_dict["TrackReleaseYear"]),
                        release_date=row_dict["TrackReleaseDate"],
                        artist=artist,
                        album=album,
                        album_artist=album_artist
                    )
                )
            if len(tracks) > 0:
                return tracks
            else:
                return False
        else:
            return False

    except Exception as e:  # Changed from sqlite.Error to catch any issues
        logger.info("[red]Database error:", e)
        return False
