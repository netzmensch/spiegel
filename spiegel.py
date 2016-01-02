#!/usr/bin/env python3
import youtube_dl
import os.path
import sys
from os import listdir
from os.path import isfile, join
import requests
import config


def download_video(url, current_path):
    meta_data = {}
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    video = ydl.extract_info(url)

    meta_data["id"] = video["id"]
    meta_data["title"] = video["title"]
    meta_data["description"] = video["description"]
    meta_data["tags"] = video["tags"]
    meta_data["file_name"] = [f for f in listdir(current_path) if isfile(join(current_path, f)) and f.find(meta_data["id"]) == 0][0]

    return meta_data

def get_youtube_access_token(client_id, client_secret, refresh_token):
    result = requests.post(
        "https://accounts.google.com/o/oauth2/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        headers={
            "content-type": "application/x-www-form-urlencoded"
        }
    )

    return result.json()["access_token"]

def get_youtube_upload_location(meta_data, access_token, api_key):
    data = \
        '{ "snippet": ' \
            '{ "title": "' + meta_data["title"] + '", ' \
            '"description": "' + meta_data["description"] + '", ' \
            '"tags": [], ' \
            '"categoryId": 20}, ' \
            '"status": { "privacyStatus": "unlisted"}}'
    pre_upload_result = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", params={
        "uploadType": "resumable",
        "part": "snippet, status",
        "key": api_key,
    }, data=data, headers={"content-type": "application/json", "Authorization": "Bearer {}".format(access_token)})

    return pre_upload_result.headers["Location"]

def upload_video(file_name, access_token):
    file_data = open(file_name, 'rb').read()
    return requests.post(
        upload_location, headers={"Authorization": "Bearer {}".format(access_token)}, data=file_data).json()["id"]

current_path = os.path.abspath(os.path.dirname(__file__))
url = sys.argv[1]

print("[download video]")
meta_data = download_video(url, current_path)

print("[get access token]")
access_token = get_youtube_access_token(config.client_id, config.client_secret, config.refresh_token)


print("[get youtube upload location]")
upload_location = get_youtube_upload_location(meta_data, access_token, config.api_token)

print("[upload video]")
youtube_id = upload_video(meta_data["file_name"], access_token)

print("[delete temp data]")
os.remove(meta_data["file_name"])

print()
print("URL: https://www.youtube.com/watch?v=" + youtube_id)