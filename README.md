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
- Supports verbose/debug logging

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

* `REKORDBOX_MASTERDB_PATH` – full path to your Rekordbox SQLite DB
* `REKORDBOX_MASTERDB_PASSWORD` – the password for decrypting the SQLite DB
* `DISCOGS_TOKEN` – your Discogs API token (follow [this guide](#getting-a-discogs-api-token) to get token)
* `VARIOUS_ARTIST_NAME` – the name used to represent various artist releases
* `INCLUDE_NO_HITS=true|false` – whether to write tracks with no hits (in Discogs) to the output CSV
* `INCLUDE_MULTIPLE_HITS=true|false` – whether to allow for multiple hits (in Discogs) for the same track to be written to the output CSV

> 🔐 Note: Your Rekordbox database must be decrypted using your master password.

### Getting a Discogs API Token

To use the Discogs API, you'll need a personal access token. Here's how to get one:

1. Go to [https://www.discogs.com](https://www.discogs.com) and log into your account.
2. Click your avatar in the top-right corner and select **Settings**.
3. In the sidebar, click **Developers**.
4. Scroll to the section **"Just need a personal access token?"** and click **Generate token**.
5. Copy the token and paste it into your `.env` file under `DISCOGS_TOKEN`.

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
- `-v` or `-vv`: Enable verbose or debug logging

Example:

```bash
poetry run discogs2rb -vv
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
