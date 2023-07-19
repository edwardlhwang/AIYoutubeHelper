import os
import requests
import openai
import re
import json
from flask import Flask, redirect, render_template, request, url_for
import googleapiclient.discovery

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        videoLink = request.form["videoLink"]
        videoId = get_video_id(videoLink)
        videoComments = get_youtube_comments(videoId)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "{}".format(generate_prompt(videoComments))}],
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0]['message']['content']))
    
    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(videoComments):
    return """Given the following list of youtube comments, provide a rating of the video that they are commenting from 0-100. Please also give a short explanation. {}""".format(videoComments)



def get_youtube_comments(video_id):
    """Gets all the comments on a YouTube video.

    Args:
    video_id: The ID of the YouTube video.

    Returns:
    A list of dictionaries, where each dictionary represents a comment.
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=50
    )
    response = request.execute()

    comments = []
    for comment_thread in response['items']:
        comments.append(comment_thread["snippet"]["topLevelComment"]["snippet"]["textOriginal"])

    print(comments)
    return comments
  
def get_video_id(link):
    """Gets the video ID from a YouTube link.

    Args:
        link: The YouTube link.

    Returns:
        The video ID.
    """

    match = re.search(r"watch\?v=(.*)", link)
    if match:
        return match.group(1)
    else:
        return None