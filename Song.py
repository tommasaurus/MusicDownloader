import os 
from youtube_search import YoutubeSearch
from pytube import YouTube, Playlist
import ssl
import json
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment

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

def enhance_audio(audio_clip):
    # Convert moviepy AudioFileClip to pydub AudioSegment
    audio_segment = AudioSegment.from_file(audio_clip.fps, audio_clip.nchannels, audio_clip.to_soundarray())
    
    # Apply some enhancements (you can customize this part)
    # For example, normalize the audio and apply a low-pass filter
    audio_segment = audio_segment + 10  # Increase volume by 10 dB
    audio_segment = audio_segment.low_pass_filter(1000)  # Apply low-pass filter

    return audio_segment

def download_and_convert_to_mp3(video_url, path = None):
    # Create a YouTube object
    ssl._create_default_https_context = ssl._create_unverified_context
    yt = YouTube(video_url)

    # Get the best audio stream
    audio_stream = yt.streams.filter(only_audio=True, file_extension='webm').order_by('abr').first()

    # Set the output file name
    song_title = audio_stream.title + ".mp3"

    # Download and convert to MP3
    audio_clip = AudioFileClip(audio_stream.url)
    
    if path:
        audio_file_path_mp3 = os.path.join(path, song_title)
    else:
        audio_file_path_mp3 = os.path.join(music_folder_path, song_title)

    enhanced_audio_clip = enhance_audio(audio_clip)
    audio_clip.write_audiofile(enhanced_audio_clip)

def download(video_url):
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

def search(song_title):
    ssl._create_default_https_context = ssl._create_unverified_context
    results = YoutubeSearch(song_title, max_results=1).to_json()

    data = json.loads(results)
    if len(data["videos"]) > 0:
        first_video_id = data["videos"][0]["id"]
        video_url = "https://www.youtube.com/watch?v=" + first_video_id

        download(video_url)
        return True
    return False

def download_album(playlist_url, new_folder = False):
    # Create a Playlist object
    ssl._create_default_https_context = ssl._create_unverified_context
    playlist = Playlist(playlist_url)

    album_path = ""
    if new_folder:
        album_path = os.path.join(music_folder_path, playlist.title)

        if not os.path.exists(album_path):
            os.makedirs(album_path)
            print(f"The '{album_path}' folder has been created on the desktop.")
        else:
            print(f"The '{album_path}' folder already exists on the desktop.")


    # Iterate through each video in the playlist
    for video_url in playlist.video_urls:
        # Download and convert each video to MP3
        download_and_convert_to_mp3(video_url, album_path)
    
# download_album("https://www.youtube.com/playlist?list=PLgNAVqTsP7odsw1WoIkj4D_w8NAqm9-2Q", new_folder=True)
search("monaco bad bunny")
# results = YoutubeSearch("love yourself tear", max_results=3).to_json()
# print(results)
