# Extra functions
import os
import re
import requests
import wget

# main download path default is user directory
main_path = os.path.expanduser("~")

def banner():
    # App banner
    return "Anime Downloader 1.0"

def not_valid_episodes(episodes):
    # Verify episode
    try:
        episodes = episodes.split(":")
        if len(episodes) == 1:
            if int(episodes[0]) > 0:
                return False
        if len(episodes) == 2:
            if int(episodes[0]) > 0 and (int(episodes[1]) > 0 or int(episodes[1]) == -1):
                return False
    except:
        return True
    return True

def get_kwik(url):
    # Convert kwik url to mp4
    url = url.replace("https://kwik.cx/e/", "https://kwik.cx/f/")
    s = requests.Session()
    parts_re = re.compile(r'action=\"([^"]+)\".*value=\"([^"]+)\".*Click Here to Download', re.DOTALL)
    kwik_text = s.get(url, headers={"referer": url}).text
    post_url, token = parts_re.search(kwik_text).group(1, 2)
    kwik_url = s.post(post_url, data={"_token": token}, headers={"referer": url}, allow_redirects=False).headers["location"]
    return kwik_url

def get_quality(quality, qualities):
    # Get quality of file to download
    if quality in qualities:
        return quality
    elif len(qualities) == 1:
        return qualities[0]
    else:
        quality = int(quality[:-1])
        distances = list(map(lambda x: abs(int(x[:-1]) - quality), qualities))
        lowest_distance = distances.index(min(distances))
        return qualities[lowest_distance]

def init_download(anime_title):
    # Initialize download folder
    if not os.path.exists(os.path.join(main_path, anime_title)):
        print("\nCreating download path...")
        save_path = os.path.join(main_path, anime_title)
        os.mkdir(save_path)
        print("Saving downloaded files to '{}'".format(save_path))

def download_mp4(url, filename):
    # Download mp4 file
    print("Started downloading {}".format(os.path.basename(filename)))
    wget.download(url, filename)
    print("Finished downloading {}".format(os.path.basename(filename)))

def sanitize_dir(dir):
    # sanitizes directory path
    included_chars = list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58))
    included_chars = list(map(chr, included_chars)) + [" ", "_", "-"]
    return "".join([s for s in dir if s in included_chars])
