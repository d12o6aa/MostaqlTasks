from flask import Flask, render_template, request
from googleapiclient.discovery import build
import csv
import os

app = Flask(__name__)

API_KEY = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

CACHE_FILE = 'cache.csv'

def get_video_details(video_id):
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    items = response.get('items', [])
    if not items:
        return None
    snippet = items[0]['snippet']
    return {
        'title': snippet['title'],
        'channel_title': snippet['channelTitle'],
        'channel_id': snippet['channelId'],
        'video_id': video_id,
        'video_url': f'https://www.youtube.com/watch?v={video_id}'
    }

def check_video_in_playlist(video_id, playlist_id):
    next_page_token = None
    while True:
        response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            if item['contentDetails']['videoId'] == video_id:
                return True

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return False

def search_playlists_by_title(video_title, video_id):
    playlists = []
    next_page_token = None

    while True:
        response = youtube.search().list(
            part='snippet',
            q=video_title,
            type='playlist',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            playlist_id = item['id']['playlistId']
            if check_video_in_playlist(video_id, playlist_id):
                playlist = {
                    'playlist_title': item['snippet']['title'],
                    'channel_title': item['snippet']['channelTitle'],
                    'channel_id': item['snippet']['channelId'],
                    'playlist_id': playlist_id
                }
                playlists.append(playlist)
                save_result_to_csv(video_id, playlist, data_type='playlist')

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return playlists

def save_result_to_csv(video_id, data, data_type='playlist'):
    file_exists = os.path.isfile(CACHE_FILE)

    with open(CACHE_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['video_id', 'type', 'playlist_id', 'playlist_title', 'channel_title', 'channel_id'])
        if data_type == 'playlist':
            writer.writerow([
                video_id,
                'playlist',
                data.get('playlist_id', ''),
                data.get('playlist_title', ''),
                data.get('channel_title', ''),
                data.get('channel_id', '')
            ])
        elif data_type == 'channel':
            writer.writerow([
                video_id,
                'channel',
                '',
                '',
                data.get('channel_title', ''),
                data.get('channel_id', '')
            ])

def get_cached_results_from_csv(video_id):
    if not os.path.isfile(CACHE_FILE):
        return []

    with open(CACHE_FILE, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        results = []
        for row in reader:
            if row['video_id'] == video_id:
                results.append({
                    'type': row['type'],
                    'playlist_id': row['playlist_id'],
                    'playlist_title': row['playlist_title'],
                    'channel_title': row['channel_title'],
                    'channel_id': row['channel_id']
                })
        return results


def save_channel_data(video_details):
    channel_data = {
        'channel_title': video_details['channel_title'],
        'channel_id': video_details['channel_id']
    }
    save_result_to_csv(video_details['video_id'], channel_data, data_type='channel')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_id = request.form['video_id'].strip()
        video_details = get_video_details(video_id)

        if not video_details:
            return render_template('result.html', results=None, video=None, error="لم يتم العثور على الفيديو.")

        cached_results = get_cached_results_from_csv(video_id)
        if cached_results:
            return render_template('result.html', results=cached_results, video=video_details, error=None)

        playlists = search_playlists_by_title(video_details['title'], video_id)
        if not playlists:
            save_channel_data(video_details)
            cached_results = get_cached_results_from_csv(video_id)
            return render_template('result.html', results=cached_results, video=video_details, error=None)

        return render_template('result.html', results=playlists, video=video_details, error=None)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
