import os 
from youtube_search import YoutubeSearch
from pytube import YouTube, Playlist
import ssl
import json
from moviepy.editor import VideoFileClip, AudioFileClip

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
music_folder_name = 'Music'
music_folder_path = os.path.join(desktop_path, music_folder_name)

if not os.path.exists(music_folder_path):
    os.makedirs(music_folder_path)
    print(f"The '{music_folder_name}' folder has been created on the desktop.")
else:
    print(f"The '{music_folder_name}' folder already exists on the desktop.")

def convert_webm_to_mp3(input_path, output_path):
    video_clip = VideoFileClip(input_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    video_clip.close()

def search(song_title):
    results = YoutubeSearch(song_title, max_results=1).to_json()

    data = json.loads(results)
    if len(data["videos"]) > 0:
        ssl._create_default_https_context = ssl._create_unverified_context
        first_video_id = data["videos"][0]["id"]
        video_url = "https://www.youtube.com/watch?v=" + first_video_id

        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='webm').order_by('abr').first()
        
        print(audio_stream.title)
        song_title = audio_stream.title + ".mp3"

        audio_clip = AudioFileClip(audio_stream.url)
        audio_file_path_mp3 = os.path.join(music_folder_path, song_title)
        audio_clip.write_audiofile(audio_file_path_mp3)
        return True
    return False

def download_album(playlist_url):
    # Create a Playlist object
    playlist = Playlist(playlist_url)

    # Iterate through each video in the playlist
    for video_url in playlist.video_urls:
        # Download and convert each video to MP3
        download_and_convert_to_mp3(video_url)

def download_and_convert_to_mp3(video_url):
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the best audio stream
    audio_stream = yt.streams.filter(only_audio=True, file_extension='webm').order_by('abr').first()

    # Print the title of the video
    print(audio_stream.title)

    # Set the output file name
    song_title = audio_stream.title + ".mp3"

    # Download and convert to MP3
    audio_clip = AudioFileClip(audio_stream.url)
    audio_file_path_mp3 = os.path.join(music_folder_path, song_title)
    audio_clip.write_audiofile(audio_file_path_mp3)

search("impossible")