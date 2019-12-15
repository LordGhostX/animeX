# our friendly neighbourhood imports :)
import os
import re
import wget
import requests

def search_anime(name, source="animepahe"):
    # search for requested anime
    def animepahe(name):
        # search animepahe.com
        # get search URL
        search_url = "https://animepahe.com/api?m=search&l=8&q=" + name
        data = requests.get(search_url).json()
        # if there's no search result return nothing
        if data["total"] <= 0:
            return None
        # return anime info
        search_data = []
        for i in data["data"]:
            anime_id = i["id"]
            anime_url = "https://animepahe.com/anime/" + i["slug"]
            anime_title = i["title"]
            anime_episodes = i["episodes"]
            anime_rating = i["score"]
            search_data.append({"id": anime_id, "url": anime_url, "title": anime_title, "no_episodes": anime_episodes, "rating": anime_rating})
        return search_data

    url_map = {"animepahe": animepahe}
    return url_map[source](name)

def get_episodes(anime_id, source="animepahe"):
    # get episodes of anime
    def get_kwik(url):
        url = url.replace("https://kwik.cx/e/", "https://kwik.cx/f/")
        s = requests.Session()
        parts_re = re.compile(r'action=\"([^"]+)\".*value=\"([^"]+)\".*Click Here to Download', re.DOTALL)
        kwik_text = s.get(url, headers={"referer": url}).text
        post_url, token = parts_re.search(kwik_text).group(1, 2)
        kwik_url = s.post(post_url, data={"_token": token}, headers={"referer": url}, allow_redirects=False).headers["location"]
        return kwik_url

    def animepahe(anime_id):
        # get animepahe.com episodes
        episodes = []
        page_url = "https://animepahe.com/api?m=release&id={}".format(anime_id)
        page_data = requests.get(page_url).json()
        for i in range(page_data["last_page"]):
            episode_url = "https://animepahe.com/api?m=release&id={}&page={}".format(anime_id, i + 1)
            episode_data = requests.get(episode_url).json()
            for episode in episode_data["data"]:
                episode_id = episode["id"]
                video_url = "https://animepahe.com/api?m=embed&p=kwik&id={}".format(episode_id)
                video_data = requests.get(video_url).json()
                episode_url = get_kwik(video_data["data"][str(episode_id)]["720p"]["url"])
                episodes.append({"id": episode_id, "title": episode["anime_title"], "episode_num": episode["episode"], "url": episode_url})
        return episodes[::-1]

    url_map = {"animepahe": animepahe}
    return url_map[source](anime_id)

def check_exists(data, main_path, filename):
    # create the anime folder to download to
    if not os.path.exists(os.path.join(main_path, data["title"])):
        os.mkdir(os.path.join(main_path, data["title"]))
    # if the file exists, skip
    if os.path.exists(filename):
        if os.path.exists(filename + ".tmp"):
            return True
        return False
    return True

def download_episode(data):
    # download anime episodes
    def download(url, filename):
        open(filename + ".tmp", "w").write("Downloading...")
        wget.download(url, filename)
        os.remove(filename + ".tmp")

    print("Starting download of {} episode {}".format(data["title"], data["episode_num"]))
    main_path = os.path.expanduser("~")
    filename = os.path.join(main_path, data["title"], "{} {}.mp4".format(data["title"], data["episode_num"]).replace(" ", "_"))
    if check_exists(data, main_path, filename):
        download(data["url"], filename)

    print("Finished downloading {} episode {}".format(data["title"], data["episode_num"]))

def main(name, source="animepahe", episode=None):
    # download requested anime
    anime_data = search_anime(name, source.lower())
    # if we have search results, proceed
    if anime_data:
        # print gotten anime
        print("Search results for {} from {}\n".format(name, source))
        for i, j in enumerate(anime_data):
            print("{}. {} - {} rating".format(i + 1, j["title"], j["rating"]))
        print()
        # ask user for choice
        while True:
            try:
                # keep asking till choice is valid
                choice = int(input("Enter the anime no:  [1]: "))
                if choice < len(anime_data) or choice > len(anime_data):
                    continue
                break
            except KeyboardInterrupt:
                exit()
            except:
                pass
        anime_data = anime_data[choice - 1]
    else:
        return "Couldn't find requested anime on " + source

    print("Getting episode data")
    episodes = get_episodes(anime_data["id"], source)
    if episode:
        episode_data = episode.split(":")
        if len(episode_data) == 1:
            episodes = [episodes[int(episode_data - 1)]]
        else:
            episodes = episodes[int(episode_data[0]) -1:int(episode_data[1]) -1]

    print("Downloading episodes")
    for i in episodes:
        download_episode(i)

print(main(input("Search for anime: ")))
