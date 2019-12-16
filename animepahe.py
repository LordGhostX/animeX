# AnimePahe Download Manager
import os
import requests
from extras import *

class AnimePahe():
    def __init__(self):
        self.source = "AnimePahe"
        self.url = "https://animepahe.com"
        self.api = "https://animepahe.com/api"

    def search(self, anime_title):
        # Query animepahe search api for relevant anime titles
        params = {
            "m": "search",
            "l": 8,
            "q": anime_title
        }
        data = requests.get(self.api, params=params).json()

        # Return nothing if there's no data from the query
        if data["total"] == 0:
            return None

        search_data = []
        for d in data["data"]:
            search_data.append(d)
        return search_data

    def get_anime_data(self, anime_title):
        # Get all data from an anime
        search_result = self.search(anime_title)
        if search_result == None:
            return None
        else:
            # Display search results for user to select from
            print("Search results for '{}' from {}".format(anime_title, self.source))
            for i, j in enumerate(search_result):
                print("{}. {} - {}".format(i + 1, j["title"], self.source))
            choice = int(input("\nEnter the anime no:  [1]: "))
            anime_data = search_result[choice - 1]
            init_download(anime_data["title"])

            return anime_data

    def get_stream_url(self, episode, quality):
        # Get mp4 url to stream anime from
        params = {
            "m": "embed",
            "p": "kwik",
            "id": episode["id"]
        }
        data = requests.get(self.api, params=params).json()

        # Get video quality to download
        quality = get_quality(quality, list(data["data"][str(episode["id"])].keys()))

        # get streaming url
        pre_sream_url = data["data"][str(episode["id"])][quality]["url"]
        stream_url = get_kwik(pre_sream_url)
        return stream_url

    def download_episodes(self, anime_data, episodes, quality):
        # Download anime episodes
        params = {
            "m": "release",
            "id": anime_data["id"]
        }
        data = requests.get(self.api, params=params).json()
        last_page = data["last_page"]

        # Construct episodes to download
        if len(episodes.split(":")) == 1:
            start = end = int(episodes.split(":")[0])
        else:
            start, end = list(map(int, episodes.split(":")))

        # Go through each anime episode page
        for i in range(last_page, 0, -1):
            params = {
                "m": "release",
                "id": anime_data["id"],
                "page": i
            }
            data = requests.get(self.api, params=params).json()

            # Go through each anime on the page
            for episode in data["data"][::-1]:
                episode_num = int(episode["episode"])
                # Check if the current episode is among the ones we want to download
                if episode_num >= start and episode_num <= end:
                    # Get the mp4 url of the episode
                    stream_url = self.get_stream_url(episode, quality)
                    # Generate the filename to save the video
                    filename = os.path.join(main_path, anime_data["title"], "{} {}.mp4".format(anime_data["title"], episode_num).replace(" ", "_"))
                    # If the file already exists skip it, else download
                    if not os.path.exists(filename):
                        download_mp4(stream_url, filename)

    def download_anime(self, anime_title, episodes="1:-1", quality="720p"):
        # Download requested anime
        if not_valid_episodes(episodes):
            # verify if episode is valid
            print("Invaid episode format")
            print("Episode format - start:end\t1:-1 will download all episodes")
            raise Exception("Invalid episode format")
        print("\nGetting anime info...")
        anime_data = self.get_anime_data(anime_title.lower())
        if anime_data == None:
            print("Couldn't find '{}' on {}".format(anime_title, self.source))
            return
        else:
            print("\nGetting episodes info...")
            self.download_episodes(anime_data, episodes, quality)
