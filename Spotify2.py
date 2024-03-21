import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = 'playlist-modify-public'
username = 'Tommasaurus1703'



token = SpotifyOAuth(scope=scope, username=username)
spot = spotipy.Spotify(auth_manager=token)


playlistName = input("What would you like to name the Playlist?: ")
description = input('Enter the playlist description:')

spot.user_playlist_create(user=username, name=playlistName, public= True, description=description)

userSong = input("Enter a Song: ")
songs = []

while userSong != 'q':
    result = spot.search(q=userSong)
    json.dumps(result, sort_keys=4, indent=4)
    songs.append(result['tracks']['items'][0]['uri'])
    userSong = input('Enter a Song:')

prePlaylist = spot.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

spot.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=songs)