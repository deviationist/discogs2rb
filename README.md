# discogs2rb

**discogs2rb** is a command-line utility designed for DJs who use **Rekordbox** and want to enhance their music library with accurate album and artist metadata from **Discogs**. The script connects to the encrypted Rekordbox SQLite database, identifies tracks missing album or album artist information, and attempts to enrich the metadata using the Discogs API.

> ✅ This tool is built with [Poetry](https://python-poetry.org/) for dependency management and includes development tools like `black`, `ruff`, and `mypy`.

---

## Features

- Connects to the encrypted Rekordbox database using `pysqlcipher3`
- Queries tracks missing album or album artist metadata
- Uses the Discogs API to resolve metadata
- Automatically handles API rate limits (60 requests per minute)
- Writes enriched metadata to a `output.csv` file
- Supports dry-run mode and verbose/debug logging

---

## CSV Output

When finished, all resolved tracks will be written to a file named `output.csv` in the project root. The file includes the following columns:

```text
TrackID, TrackTitle, TrackArtist, AlbumTitle, AlbumArtists, ReleaseYear, ReleaseDate, ReleaseURL, Artwork
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/deviationist/discogs2rb.git
cd discogs2rb
```

### 2. Configure Environment Variables

Copy the `.env.example` file and fill in the required values:

```bash
cp .env.example .env
```

Edit `.env` with your preferred text editor:

```env
REKORDBOX_MASTERDB_PATH="/path/to/rekordbox/master.db"
REKORDBOX_MASTERDB_PASSWORD=""
DISCOGS_TOKEN=""
VARIOUS_ARTIST_NAME="Various Artists"
```

> 🔐 Note: Your Rekordbox database must be decrypted using your master password.

### 3. Install Dependencies

Make sure [Poetry](https://python-poetry.org/docs/#installation) is installed.

```bash
poetry install
```

---

## Running the Script

To run the metadata resolution script:

```bash
poetry run discogs2rb
```

### Optional Arguments

- `--dry-run`: Run the script without writing to the output CSV
- `-v` or `-vv`: Enable verbose or debug logging

Example:

```bash
poetry run discogs2rb --dry-run -vv
```

---

## Development

This project uses the following tools for code quality:

- [**Black**](https://black.readthedocs.io/en/stable/): Code formatter
- [**Ruff**](https://docs.astral.sh/ruff/): Linter
- [**mypy**](http://mypy-lang.org/): Static type checker

To run formatters and linters:

```bash
poetry run black .
poetry run ruff check .
poetry run mypy .
```

---

## Notes

- Discogs enforces a strict API rate limit (60 requests per minute). The script will automatically wait when needed to avoid hitting this limit.
- The script may take some time to complete if many tracks need to be resolved.

---

## License

MIT License

---

## Author

[@deviationist](https://github.com/deviationist)

Project URL: [https://github.com/deviationist/discogs2rb](https://github.com/deviationist/discogs2rb)
