# our friendly neighbourhood imports :)
from animepahe import AnimePahe
from extras import banner, init_download

def main():
    site_map = {"1": AnimePahe}
    quality_map = ["360p", "480p", "720p", "1080p"]

    print(banner())

    print("\nChoose where to download anime from")
    print("1. AnimePahe")
    choice = input("\nEnter the site no:  [1]: ")
    downloader = site_map[choice]()

    anime_title = input("\nEnter anime title: ")
    episode_start = input("\nEnter starting episode: 1 for first: ")
    episode_end = input("\nEnter ending episode: -1 for last: ")

    print("\nChoose quality of video to download")
    for i, j in enumerate(quality_map):
        print("{}. {}".format(i + 1, j))
    choice = int(input("\nEnter the quality no:  [1]: "))
    quality = quality_map[choice - 1]

    downloader.download_anime(anime_title, "{}:{}".format(episode_start, episode_end), quality)

if __name__ == "__main__":
    main()
