from .. import config
from ..utils.helpers import get_boolenv
from ..utils.logger import logger
from ..utils.progress_bar import progress_instance
from ..rekordbox.resolvers.track import get_tracks_with_missing_album
from ..discogs.discogs_client import search_release_metadata
import csv


class ResolveDiscogsTracks:
    def exec(self):
        folders_to_ignore = config.get_folders_to_ignore()
        tracks = get_tracks_with_missing_album(folders_to_ignore)
        if not tracks:
            raise Exception("Could not get any tracks from DB.")
        track_count = len(tracks)
        resolved_tracks_count = 0
        resolved_tracks = []
        include_no_hits = get_boolenv("INCLUDE_NO_HITS", True)
        allow_multiple_hits = get_boolenv("INCLUDE_MULTIPLE_HITS", True)
        with progress_instance() as progress:
            logger.info(
                f"[cyan]Attempting to resolve {track_count} tracks metadata in Discogs..."
            )
            task = progress.add_task("", total=track_count)
            for track in tracks:
                track_string = f'"{track.title}" by "{track.artist.name}"'
                progress.update(
                    task,
                    description=f"[yellow]Resolving track metadata for track {track_string}",
                )
                releases = search_release_metadata(
                    track.title, track.artist.name, allow_multiple_hits
                )
                if releases:
                    for release in releases:
                        resolved_tracks.append(
                            [
                                track.id,
                                track.title,
                                track.artist.name,
                                release.album_title,
                                release.album_artists,
                                "Yes" if release.is_various else "No",
                                release.release_year,
                                release.release_date,
                                release.release_url,
                                release.image,
                            ]
                        )
                        resolved_tracks_count += 1
                    progress.update(
                        task,
                        advance=1,
                        description=f"[yellow]Resolved track metadata for track {track_string}...",
                    )
                else:
                    if include_no_hits:
                        resolved_tracks.append(
                            [
                                track.id,
                                track.title,
                                track.artist.name,
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                            ]
                        )
                    progress.update(
                        task,
                        advance=1,
                        description=f"[red]Could not resolve track metadata for track {track_string}...",
                    )
            progress.update(
                task,
                description=f"[bold green]✔ Done! Resolved {resolved_tracks_count} Discogs-track(s) from {track_count} Rekordbox-track(s)!",
            )
        logger.info("[cyan]Writing result to CSV-file...")
        self.write_csv(resolved_tracks)

    def write_csv(self, resolved_tracks):
        header_columns = [
            "TrackID",
            "TrackTitle",
            "TrackArtist",
            "AlbumTitle",
            "AlbumArtists",
            "IsVarious",
            "ReleaseYear",
            "ReleaseDate",
            "ReleaseURL",
            "Artwork",
        ]
        data = [header_columns] + resolved_tracks
        try:
            with open("output.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)
                logger.info("[cyan][bold green]✔ Done!")
        except Exception as e:
            logger.error(f"[Exception] {e}")
            return None
