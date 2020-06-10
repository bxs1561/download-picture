import requests
from bs4 import BeautifulSoup
import json
import random
import os
import lxml
import re
import pytube
import youtube_dl
import requests


# import imdb
# imdb only compatable with python 2.7


def instagram_graphql():
    # user_name = ''
    user_name = input('enter username of instagram : ')

    inst_url = 'https://www.instagram.com'
    last_url = '?__a=1'

    res = requests.get(f"{inst_url}/{user_name}/{last_url}")
    # url = 'https://www.instagram.com/<user_name>/?__a=1'
    data = res.json()
    full_name = data['graphql']['user']['full_name']
    print("full name: " + " " + full_name)
    print("folower:" + " " + str(data['graphql']["user"]["edge_followed_by"]['count']))
    # print(data['graphql']['user']['profile_pic_url_hd'])
    profile_pic = data['graphql']['user']['profile_pic_url_hd']

    # download profile picture in file
    file_name = full_name + str(random.randint(1, 100000)) + '.jpeg'
    file_exist = os.path.isfile(file_name)
    if not file_exist:
        with open(file_name, 'wb+') as handle:
            response = requests.get(profile_pic, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)


# find the some details from insta without intagram graphql api
def insta_url():
    url = "https://www.instagram.com/{}/"
    return url


# parse function
def parse_data(s):
    data = {}
    s = s.split("-")[0]
    s = s.split(" ")

    data['Followers'] = s[0]
    data['Following'] = s[2]
    data['Posts'] = s[4]

    return data


def scrape_data(username):
    r = requests.get(insta_url().format(username))
    print(insta_url().format(username))
    s = BeautifulSoup(r.text, "html.parser")
    meta = s.find("meta", property="og:description")

    return parse_data(meta.attrs['content'])


def youtube_data_filter(search_query, filter):
    link = 'https://www.youtube.com/results?search_query={}'
    links = requests.get(link.format(search_query))
    html = links.content
    html_parser = BeautifulSoup(html, 'html.parser')
    # videos_list = html_parser.findAll('ol', {'class': 'item-section'})
    # videos_list = html_parser.findAll('div', {'id': 'content'})
    # videos_list = html_parser.findAll('div', {'id': 'results'})
    videos_list = html_parser.findAll('div', {'class': 'filter-col'})

    # videos_list = html_parser.findAll('div', {'class': 'yt-lockup-thumbnail contains-addto'})

    #
    video_img = videos_list[0]

    complete_link_last_hr = " "
    link_today = " "
    link_week = " "
    link_month = " "
    for filters in videos_list:
        search_url = filters.ul
        youtube = "https://youtube.com{}"

        for search in search_url:
            try:
                url_query = search.a['href']
                if "Last hour" in search.text and filter == "last hour":
                    complete_link_last_hr += youtube.format(url_query).replace(',', '')
                    return complete_link_last_hr
                elif "Today" in search.text and filter == "today":
                    link_today += youtube.format(url_query).replace(',', '')
                    return link_today
                elif "This week" in search.text and filter == "this week":
                    link_week += youtube.format(url_query).replace(',', '')
                    return link_week
                elif "This month" in search.text and filter == "this month":
                    link_month += youtube.format(url_query).replace(',', '')
                    return link_month
            except IndexError as error:
                print(error.args)
            except:
                continue


def youtube_vide_data(search):
    link = 'https://www.youtube.com/results?search_query={}'
    links = requests.get(link.format(search))
    html = links.content
    html_parser = BeautifulSoup(html, 'html.parser')
    videos_list = html_parser.findAll('div', {'class': 'yt-lockup-dismissable yt-uix-tile'})

    videos = videos_list
    video_links = []
    for video in videos:
        upload = video.findAll('div', {'class': 'yt-lockup-meta'})
        descriptions = video.findAll('h3', {'class': 'yt-lockup-title'})

        video_descriptions = descriptions[0].text
        video_link = "https://www.youtube.com{}"
        user = video.a['href']
        # print(video_link.format(user)+ video_descriptions + upload[0].text)
        # video_links += video_link.format(user)+ video_descriptions + '\n'
        video_links.append(video_link.format(user) + video_descriptions)
        # video_links = [vid]

    return video_links


def download_youtube_video(link):
    # save_video = os.mkdir('save')
    save = '/Users/bikramsubedi/PycharmProjects/download_picture'
    videos = pytube.YouTube(link)
    video = videos.streams.filter(progressive=True, file_extension='mp4')
    # audio = videos.streams.filter(only_audio=True).first()

    download_video = video.get_highest_resolution()
    # audio.download(save)
    print("downloading....")
    if download_video.download(save):
        print('download finish')


def youtube_download_using_youtube_dl(search):
    ydl_opts = {}
    # for mp3
    # bestvideo for best video
    # ydl_opts = {
    #     'format': 'bestvideo/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }],
    # }
    # ydl_opts = {
    #     'format': 'bestvideo/best'+'bestaudio/best'
    #
    # }
    # ydl_opts = {
    #     '-f': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
    # }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search])


def download_content_from_website():
    url = ''
    r = requests.get(url)
    html = BeautifulSoup(r.content, 'html.parser')
    links = html.findAll('a')

def main():
    search = input("Please enter search term: ")
    vide0 = youtube_vide_data(search)[0]
    download_youtube_video(vide0)
    # youtube_download_using_youtube_dl(vide0)

    # download_video_series(vide0)
    # print(youtube_vide_data(search))
    # 'https://barristerbabu.su/mahabharat-10th-june-2020-video-episode-47/'
    # video = download_content_from_website()
    # download_video_series(video)

    # youtube_download_using_youtube_dl(search)

    # print(youtube_vide_data(search))
    # link = input("Please enter url link to download: ")
    # download_youtube_video(link)
    # while True:
    #     search_query = input("please enter country name to search: ")
    #     filter = input("Search for last hour, today, this week or this minth: ")
    #     print(youtube_data_filter(search_query, filter))
    #     cont = input("do you wanna continue: ")
    #     if cont == "yes":
    #         search_query = input("please enter country name to search: ")
    #         filter = input("Search for last hour, today, this week or this minth: ")
    #         print(youtube_data_filter(search_query, filter))
    #         cont = input("do you wanna continue: ")
    #     if cont == "no":
    #         break

    # username = input("enter user name: ")
    # if username == "":
    #     print("please enter user name")
    # else:
    #     data = scrape_data(username)
    #     print(username + "{")
    #     print("\tFollowers:" + " " + data.get("Followers"))
    #     print("\tFollowing:" + " " + data.get("Following"))
    #     print("\tPosts:" + " " + data.get("Posts"))
    #     print("}")

    # instagram_graphql()


# run programs
if __name__ == '__main__':
    main()
