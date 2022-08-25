import math

from secret import naver
import urllib.request
import urllib.error
import urllib.parse
import json

from collections import deque
import elasticsearch7
from elasticsearch7 import helpers

import time

client_id = naver.CLIENTID
client_pw = naver.CLIENTPASSWORD

def get_blog_page(query, display):
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

            # http 오류가 안날 최대 개수 900
            if total_news_count >= 900:
                news_count = 900
            else:
                news_count = total_news_count

    return news_count


def get_blog_content(query, idx, display):
    contents = {}

    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query + \
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

    return contents

def readline(all_data):
    for line in all_data:
        yield line


def push_elasticsearch(data, idx):

    # es.indices.delete(index=idx, ignore=404)
    deque(helpers.parallel_bulk(es, readline(data), index=idx), maxlen=0)
    es.indices.refresh()


if __name__ == '__main__':
    query = "곡성군"
    display = 100
    start = 1

    page_count = get_blog_page(query, display)
    print(page_count)

    all_contents = []
    all_text = ""
    es = elasticsearch7.Elasticsearch(["http://localhost:9200"])

    for start_idx in range(start, page_count + 1, display):
        print(start_idx)
        contents = get_blog_content(query, start_idx, display)
        push_elasticsearch(contents, "test")

    # save_json(query, all_contents)

