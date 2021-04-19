import json

file = '/Users/admin/develop/code-repository/python/dish/kuaikan/autoread/return_error.json'
comic_ids = []


def process_message(message):
    comic_id = message.split()[13][:-1]
    if comic_id not in comic_ids:
        comic_ids.append(comic_id)


with open(file, 'r') as load_f:
    load_dict = json.load(load_f)
    responses = load_dict['responses']
    print(responses[0]['took'])
    hits = responses[0]['hits']
    print(hits['total'])
    items = hits['hits']
    print(len(items))
    for item in items:
        message = item['_source']['message']
        process_message(message)

print(comic_ids)
print(len(comic_ids))

# rst_dict = json.loads(file)
# print(rst_dict)
