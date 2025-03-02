import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import string
import time

# Spotify API credentials
CLIENT_ID = "1b8782880df54ac0bdcc3288d49b5910"
CLIENT_SECRET = "8c902673311946e4b24d7ae5e9732d5b"

def sanitize(text):
    """Remove commas and newlines from text"""
    return text.replace(',', ' ').replace('\n', ' ').replace('\r', ' ')

def main():
    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Set to store unique songs
    unique_songs = set()
    count = 0
    
    print("Fetching songs from Spotify...")
    
    with open('songs.txt', 'w') as f:
        while count < 200:
            try:
                # Generate random search query
                query = random.choice(string.ascii_lowercase)
                
                # Search for tracks
                results = sp.search(q=query, type='track', limit=50, market='US')
                
                for track in results['tracks']['items']:
                    if count >= 200:
                        break
                        
                    # Get song details
                    song_name = track['name']
                    artist_name = track['artists'][0]['name']
                    preview_url = track['preview_url']
                    
                    # Skip if no preview URL or if song already exists
                    if not preview_url:
                        continue
                        
                    unique_key = f"{song_name} - {artist_name}"
                    if unique_key in unique_songs:
                        continue
                    
                    # Sanitize strings
                    song_name = sanitize(song_name)
                    artist_name = sanitize(artist_name)
                    
                    # Write to file
                    f.write(f"{song_name},{artist_name},{preview_url}\n")
                    unique_songs.add(unique_key)
                    count += 1
                    
                    print(f"\rFetched {count} songs...", end='', flush=True)
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"\nError: {str(e)}")
                continue
    
    print(f"\nDone! Fetched {count} songs.")

if __name__ == '__main__':
    main() 