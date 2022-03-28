# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from functools import reduce
from time import sleep

from bs4 import BeautifulSoup
import random
import requests
from bs4 import Tag

base_url = 'https://36kr.com'
today_36kr_url = None


def header() -> dict:
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;\
        q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }


def get_today_36kr_url():
    """8点1氪-早晚报 当天url"""
    content_list_response = requests.get("https://36kr.com/motif/337", headers=header())
    content_list_response.encoding = 'utf-8'
    content_text = content_list_response.text
    bs = BeautifulSoup(content_text, 'html.parser')
    content_list = bs.select('a.article-item-title')
    if len(content_list) == 0:
        return None
    content: Tag = content_list[0]
    href_suffix = content.attrs.get('href', None)
    if href_suffix is None:
        return None
    href = base_url + href_suffix
    return href


def get_today_36kr_content():
    """获得当天8点1氪内容"""
    url = get_today_36kr_url()
    global today_36kr_url
    today_36kr_url = url
    if url is None:
        return None
    sleep(random.randint(2, 5))
    content_response = requests.get(url, headers=header())
    content_response.encoding = 'utf-8'
    content_text = content_response.text
    bs = BeautifulSoup(content_text, 'html.parser')
    content_list: list = bs.select('strong')
    if len(content_list) == 0:
        return None
    text_list = list(map(lambda x: "* "+x.text, content_list))
    text = '\n'.join(text_list)
    return text


def get_today_36kr_content_finally():
    text = get_today_36kr_content()
    if text is None:
        return None
    return "科技早报：\n%s\n【8点1氪】%s" % (text, today_36kr_url)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_today_36kr_content_finally())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
