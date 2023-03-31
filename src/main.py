import requests
import csv
from lxml import html


class App:
    app_list = list()

    def __init__(self, name, varsion, update, android, links):
        self.name = name
        self.version = varsion
        self.update = update
        self.android = android
        self.links = links

    def __str__(self):
        return f"name:{self.name}"


def get_links(url):
    link = requests.get(url)
    data = html.fromstring(link.text)
    all_links = data.xpath('//a[@class="abs-fill"]/@href')
    links = all_links[0:BRANCH]
    return links


def crawl(url):
    apps = list()
    links = get_links(url)
    for link in links:
        app = requests.get(link)
        tree = html.fromstring(app.text)
        name = validate(tree.xpath('//meta[@property="og:image:alt"]/@content'))
        version = validate(tree.xpath('//*[@id="site_wrap"]/div/div/aside[1]/ul/li[3]/div/text()'))
        update = validate(tree.xpath('//*[@id="downloadbox"]/div/table/tbody/tr[1]/td/text()'))
        android = validate(tree.xpath('//*[@id="downloadbox"]/div/table/tbody/tr[2]/td/text()'))
        links = get_links(link)
        instance = App(name, version, update, android, links)
        apps.append(instance)
    App.app_list.append(apps)


def validate(objects):
    for obj in objects:
        tmp = obj.strip()
        if len(tmp) > 0:
            return tmp
    return "None"


ROOT_URL = 'https://www.farsroid.com/'

# ---> ----> ...
DEPTH = 0
#      /--->
# ----|---->
#      \--->
BRANCH = 3

crawl(ROOT_URL)

for k in range(DEPTH):
    for obj in App.app_list[k]:
        for link in obj.links:
            crawl(link)

f = csv.writer(open('./csv1.csv', 'w', encoding='utf-8'))
for depth in App.app_list:
    for app in depth:
        f.writerow([app.name, app.version, app.update, app.android])
