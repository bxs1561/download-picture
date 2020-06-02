import requests
from bs4 import BeautifulSoup as bs
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
    # profile = json.dumps(res)
    print("full name: " + " " + data['graphql']['user']['full_name'])
    print("folower:" + " " + str(data['graphql']["user"]["edge_followed_by"]['count']))
    # print(data['graphql']['user']['profile_pic_url_hd'])
    profile_pic = data['graphql']['user']['profile_pic_url_hd']

    # download profile picture in file
    file_name = 'pic' + str(random.randint(1, 100000)) + '.jpeg'
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


def main():
    instagram_graphql()


# run programs
if __name__ == '__main__':
    main()
