import os
from pathlib import Path
import base64
from requests import post, get
import json

if os.path.isfile("env.py"):
    import env

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_album(token, album_id):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"q={album_id}&type=album&limit=1"

    query_url = url + "?" + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    if len(json_result) == 0:
        print("No album found")
        return None
    
    return json_result[0]

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    tracks = []
    for item in json_result["items"]:
        track_info = {
            "track_name": item["name"],
            "track_number": item["track_number"]
        }
        tracks.append(track_info)
    return tracks

token = get_token()
result = search_for_album(token, "since+i+left+you")
album_id = result["id"]
songs = get_album_tracks(token, album_id)
print(songs)
