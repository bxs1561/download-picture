import requests
from bs4 import BeautifulSoup
import json
import random
import os.path
import lxml
import re


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
    # profile = json.dumps(res)
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
    # print(videos)
    for video in videos:
        upload = video.findAll('ul', {'class': 'yt-lockup-meta-info'})
        image = video.div.img['src']
        upload_date = upload[0].li.text

        # get views too
        # upload[0].text
        descriptions = video.findAll('div', {'class': 'yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2'})
        video_descriptions = descriptions[0].text
        video_link = "https://www.youtube.com{}"
        user = video.a['href']
        print(video_link.format(user)+ video_descriptions + upload[0].text)


def main():
    search = input("Please enter search term")
    youtube_vide_data(search)
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

    # username = ""
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
