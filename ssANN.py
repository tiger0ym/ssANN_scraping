import requests
from bs4 import BeautifulSoup
import os


def get_latest_blog():
    load_url = "https://www.allnightnippon.com/shimofuri/shimofuri_blog/"
    html = requests.get(load_url)
    bs = BeautifulSoup(html.content, "html.parser")
    return bs.find_all("a","newslist_detail")[0]

def log_check(content):
    logfile_name = "ssANN_log.txt"
    if not os.path.exists("./"+logfile_name):
        file = open(logfile_name, 'w')
    file = open(logfile_name, 'r')
    if file.readline() == content.attrs["href"]:
        checker = False
        print("False")
    else:
        checker = True
        file = open(logfile_name, 'w')
        file.write(content.attrs["href"])
        file.close()
        print("True")
    return checker

def send_line(content):
    token = "--hogehoge--"
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    message = content.find_all("p","bloglist_doc")[0].text +"\n"+ content.attrs["href"]
    payload = {'message' : message}
    p = requests.post(url, headers=headers, data=payload)

def lambda_handler(event,context):
    latest_episode = get_latest_blog()
    if log_check(latest_episode):
        send_line(latest_episode)
