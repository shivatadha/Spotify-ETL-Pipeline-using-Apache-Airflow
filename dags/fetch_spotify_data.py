import json
import os
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging


class DataIngestion:
    """Class to handle Spotify data ingestion."""

    def __init__(self, client_id, client_secret):
        """Initialize Spotify client with credentials.

        Args:
            client_id (str): Spotify API client ID
            client_secret (str): Spotify API client secret

        Raises:
            spotipy.oauth2.SpotifyOauthError: If authentication fails
        """
        try:
            self.client_id = client_id
            self.client_secret = client_secret
            self.sp = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
            )
            logging.info("Spotify client initialized successfully.")
        except spotipy.oauth2.SpotifyOauthError as e:
            logging.error(f"Authentication failed: {e}")
            raise

    def fetch_and_save_playlist_tracks(self, playlist_link, raw_data, filename=None):
        """Fetch tracks from a Spotify playlist and save to JSON.

        Args:
            playlist_link (str): URL of the Spotify playlist
            raw_data (str): Directory to save the data
            filename (str, optional): Name of the output file

        Returns:
            str: Path to the saved file

        Raises:
            Exception: If fetching or saving fails
        """
        try:
            playlist_uri = playlist_link.split("/")[-1].split('?')[0]
            logging.info(f"Fetching playlist data for URI: {playlist_uri}")

            # Fetch all tracks with pagination
            all_tracks = []
            results = self.sp.playlist_tracks(playlist_uri)
            all_tracks.extend(results['items'])

            while results['next']:
                results = self.sp.next(results)
                all_tracks.extend(results['items'])

            data = {'items': all_tracks}
            logging.info("Playlist data fetched successfully.")

            os.makedirs(raw_data, exist_ok=True)

            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"playlist_{timestamp}.json"

            file_path = os.path.join(raw_data, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Data saved to file: {file_path}")

            return file_path
        except Exception as e:
            logging.error(f"Error in fetching or saving playlist data: {e}")
            raise
