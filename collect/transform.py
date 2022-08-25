import json
from konlpy.tag import Twitter
from collections import Counter
import elasticsearch7

def count_nouns(txt):
    nouns = t.nouns(txt)
    # 글자수 min_val개 이상의 명사 추출
    min_val = 2
    processed = [n for n in nouns if len(n) >= min_val]

    count = Counter(processed)
    # 빈도가 높은 max_count 이상 명사 추출
    max_count = 26

    # 가장 갯수가 많은 것은 query
    for n, c in count.most_common(max_count)[1:]:
        all_contents[n] = c

    return all_contents

def save_json(query, content):
    from time import localtime, strftime, time

    data_dict = {
        "query": query,
        "item": content
    }
    path = "../data/blog_data"

    tm = localtime(time())
    today = strftime("%Y-%m-%d", tm)
    # path = "./data/blog_data/" + today
    #
    # try:
    #     if not os.path.isdir(path):
    #         os.mkdir(path)
    # except OSError as e:
    #     if e.errno != errno.EEXIST:
    #         print("Failed to create")
    #         raise


    with open(path + "/{}-{}.json".format(today, query), "w") as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # Elasticsearch에서 데이터 불러오기
    idx_name = "test"
    es = elasticsearch7.Elasticsearch(["http://localhost:9200"])
    res = es.search(index=idx_name, scroll='10m', size=1000)

    t = Twitter()
    items = ""
    contents = res["hits"]["hits"]
    for content in contents:
        items += (content['_source']["title"] + content['_source']["description"])

    # title과 desription에서 명서 추출 후 개수 저장
    all_contents = {}
    count_nouns(items)
    print(all_contents)

    # json으로 저장
    query = "곡성군"
    save_json(query, all_contents)



