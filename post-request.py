import requests
import json

API_ENDPOINT = "https://httpbin.org/post"

data = {'weather': 'clouds'}

r = requests.post(url=API_ENDPOINT, data=data)
# print(r.text)

url = r.text
print(url)
print("The pastebin URL is:%s" % url)
