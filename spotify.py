import os
from pathlib import Path
import base64
from requests import post, get
import json

if os.path.isfile("env.py"):
    import env

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

# Get Auth Token

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

# Search for album id

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

# Get album tracks

def get_album_tracks_with_details(token, album_id):
    # Get album details
    album_url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    album_result = get(album_url, headers=headers)
    album_json = json.loads(album_result.content)

    # Extract album details
    album_name = album_json["name"]
    album_artist = ", ".join(artist["name"] for artist in album_json["artists"])
    release_year = album_json["release_date"].split("-")[0]
    cover_image = album_json["images"][0]["url"]

    # Get album tracks
    tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    tracks_result = get(tracks_url, headers=headers)
    tracks_json = json.loads(tracks_result.content)
    tracks = []
    for item in tracks_json["items"]:
        track_info = {
            "track_name": item["name"],
            "track_number": item["track_number"]
        }
        tracks.append(track_info)

    # Return combined details
    return {
        "album_name": album_name,
        "album_artist": album_artist,
        "release_year": release_year,
        "cover_image": cover_image,
        "tracks": tracks
    }

# Example usage
token = get_token()
result = search_for_album(token, "since+i+left+you")
album_id = result["id"]
album_details = get_album_tracks_with_details(token, album_id)
print(album_details)