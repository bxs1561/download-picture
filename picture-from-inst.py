import requests
from bs4 import BeautifulSoup
import json
import random
import os.path
import lxml


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
    s = BeautifulSoup(r.text, "html.parser")
    meta = s.find("meta", property="og:description")

    return parse_data(meta.attrs['content'])


def main():
    # username = ""
    username = input("enter user name: ")

    if username == "":
        print("please enter user name")
    else:
        data = scrape_data(username)
        print(username + "{")
        print("\tFollowers:" + " " + data.get("Followers"))
        print("\tFollowing:" + " " + data.get("Following"))
        print("\tPosts:" + " " + data.get("Posts"))
        print("}")

    # instagram_graphql()


# run programs
if __name__ == '__main__':
    main()
