from qbittorrent import Client
import time

from variableConfigs import *


def get_media():
    for torrent in os.listdir(download_path):
        torrent_file = os.path.join(download_path, torrent)
        if '.torrent' in torrent_file:
            try:
                # connect to the qbittorent Web UI
                qb = Client(qb_ip)

                # put the credentials (as you configured)
                qb.login(qb_user, qb_pass)
            except Exception as e:
                raise ConnectionError(f'failed to connect to qb : {e}')

            try:
                # open and download file
                torrent_file = open(torrent_file, "rb")
                qb.download_from_file(torrent_file, savepath=media_path)
            except Exception as e:
                raise LookupError(f'file {torrent_file} not found : {e}')

    return qb


def get_size_format(b, factor=1024, suffix="B"):

    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def get_torrent_info(qb):

    # return list of torrents
    torrents = qb.torrents()

    for torrent in torrents:
        print("Torrent name:", torrent["name"])
        print("hash:", torrent["hash"])
        print("Seeds:", torrent["num_seeds"])
        print("File size:", get_size_format(torrent["total_size"]))
        print("Download speed:", get_size_format(torrent["dlspeed"]) + "/s")
        print('\n'*5)

def recursive_torrent_info(qb):
    while len(qb.torrents()) > 0:
        get_torrent_info(qb)
        time.sleep(5)

if __name__ == '__main__':
    qb = get_media()
    recursive_torrent_info(qb)