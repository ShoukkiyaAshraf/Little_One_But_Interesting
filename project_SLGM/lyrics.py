import configparser
import requests
from bs4 import BeautifulSoup


def get_access_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']


token = get_access_token()


def search_artist(name):
    api_ur = "https://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    r = requests.get(api_ur, headers=headers)
    return r.json()


def get_artist_by_id(name):
    r = search_artist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id


def get_top_ten_songs(name):
    id = get_artist_by_id(name)
    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()


def get_song_lyrics(name):
    r = get_top_ten_songs(name)
    songs = r["response"]["songs"]
    url_list = []
    for song in songs:
        url_list.append(song["url"])
    return url_list


def scrap_one_page_lyrics(page_url):
    page = requests.get(page_url)
    # print('time : {} seconds'.format(page.elapsed.total_seconds()))
    soup = BeautifulSoup(page.content, 'html.parser')
    class_lyrics = soup.find("div", class_="lyrics")
    anchor_tags = class_lyrics.find_all('a')
    current_list = []
    for anchor_tag in anchor_tags:
        if len(anchor_tag.text) > 0 and anchor_tag.text[0] != '[':
            text = anchor_tag.text.replace("\n", "NEWLINE")
            current_list.append(text)
    return current_list


def scrap_lyric_pages(name):
    links = get_song_lyrics(name)
    result = []
    for li in links:
        try:
            lyrics_li = scrap_one_page_lyrics(li)
            print('worked')
            result.append(lyrics_li)
        except:
            print('cannot load {}'.format(li))
            retry = input('do you want to try more time: (y/n)')
            while retry == 'y':
                try:
                    lyrics_li = scrap_one_page_lyrics(li)
                    result.append(lyrics_li)
                    print('worked')
                    retry = 'n'
                except:
                    print('failed try {}'.format(li))
                    print('\n')
                    retry = input('do you want to try more time: (y/n)')
                if retry == 'n':
                    break
    return result
