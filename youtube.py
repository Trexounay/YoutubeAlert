# -*- coding: utf-8 -*-

# Sample Python code for youtube.activities.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyB5B2VNlTBH39T346ZFH4C5Y4F-eqVbYgY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.activities().list(
        part="snippet,contentDetails",
        channelId="UCAG3CiKOUkQysyKCXSFEBPA",
        maxResults=5
    )
    response = request.execute()
    for i in response["items"]:
        if i["snippet"]["type"] == "upload":
            print("title:", i["snippet"]["title"])
            print("link:", "http://youtube.com/watch?v="+i["contentDetails"]["upload"]["videoId"])
            print()

if __name__ == "__main__":
    main()
