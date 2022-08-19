import math

from secret import naver
import urllib.request
import urllib.error
import urllib.parse
import json

from konlpy.tag import Twitter
from collections import Counter, defaultdict

client_id = naver.CLIENTID
client_pw = naver.CLIENTPASSWORD

def get_news_page(query, display):
    global news_count

    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/news?query=" + encode_query
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_pw)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()
    if (response_code == 200):
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))


        if response_body_dict["total"] == 0:
            news_count = 0
        else:
            total_news_count = math.ceil(response_body_dict["total"] / int(display))

            if total_news_count >= 100:
                news_count = 100
            else:
                news_count = total_news_count

    return news_count


def get_news_content(query, idx, display):
    text = ""
    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/news?query=" + encode_query + \
        "&start=" + str(idx) + "&display=" + str(display)
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_pw)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()
    if response_code == 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))
        contents = response_body_dict["items"]
        for content in contents:
            print(content["pubDate"])
            text += content["title"] + " " + content["description"]
    return text


def count_nouns(txt):
    nouns = t.nouns(txt)
    # 글자수 min_val개 이상의 명사 추출
    min_val = 2
    processed = [n for n in nouns if len(n) >= min_val]

    count = Counter(processed)
    # 빈도가 높은 max_count 이상 명사 추출
    max_count = 20

    for n, c in count.most_common(max_count):
        all_contents[n] = c

    return all_contents


if __name__ == '__main__':
    query = "남해"
    display = 100
    start = 1

    # page_count = get_news_page(query, display)
    # print(page_count)

    t = Twitter()
    all_contents = {}
    all_text = ""
    # page_count + 1
    for start_idx in range(start, 901, display):
        print(start_idx)
        all_text += get_news_content(query, start_idx, display) + " "


    print(count_nouns(all_text))

