import json
import urllib.request as req
import urllib
import requests

header = {
    'Host': 'tencn-log-search.quickcan.com',
    'Content-Type': 'application/json'}

data = [{"index": "kk-log_search_image_search-image_watermark-detect_info**", "ignore_unavailable": 'true', "preference": 1591236925290},
        {"version": 'true', "size": 5000, "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "boolean"}}], "_source": {"excludes": []}, "aggs":{"2": {"date_histogram": {"field": "@timestamp", "interval": "12h", "time_zone": "Asia/Shanghai", "min_doc_count": 1}}}, "stored_fields": ["*"], "script_fields":{}, "docvalue_fields": [{"field": "@timestamp", "format": "date_time"}], "query": {"bool": {"must": [{"match_phrase": {"additions.message": {"query": "1061370885430051520"}}}, {"range": {"@timestamp": {"format": "strict_date_optional_time", "gte": "2020-05-20T08:40:13.402Z", "lte": "2020-06-04T08:40:13.402Z"}}}], "filter": [{"match_all": {}}], "should": [], "must_not":[]}}, "highlight":{"pre_tags": ["@kibana-highlighted-field@"], "post_tags":["@/kibana-highlighted-field@"], "fields":{"*": {}}, "fragment_size": 2147483647}, "timeout": "30000ms"}]


url = 'http://tencn-log-search.quickcan.com/elasticsearch/_msearch?rest_total_hits_as_int=true&ignore_throttled=true'

data = urllib.parse.urlencode(data)
r = requests.post(url, data=data)
print(r)
