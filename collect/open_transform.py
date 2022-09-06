from opensearchpy import OpenSearch
from time import localtime, strftime, time


if __name__ == '__main__':
    query = "의왕시"
    index_name = "uiwangsi"

    # opensearch config
    host, port = "localhost", 9200
    auth = ("admin", "admin")
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        # ca_certs=ca_certs_path
    )

    before_week = strftime("%Y%m%d", localtime(time() - 604800))
    before_month = strftime("%Y%m%d", localtime(time() - 2592000))

    doc = {"query": {"range": {"postdate": {"gt": before_month}}}}

    res = client.search(
        index=index_name,
        body=doc
    )

    items = ""
    contents = res["hits"]["hits"]
    for content in contents:
        items += (content['_source']["title"] + content['_source']["description"])

    print(items)




