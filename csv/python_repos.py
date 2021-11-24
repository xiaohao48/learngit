import requests

requests.adapters.DEFAULT_RERRIES = 5
s = requests.session()
s.keep_alive = False
# url = 'https://api.github.com/search/repositories?q=language:python&sort=stars%27'
url = 'http://yapi.pinjamy.com:19013/mock/50/v1/events'
r = s.get(url)
print("status code:", r.status_code)
response_dict = r.json()
for key,value in response_dict.items():
    print(key,value)
print(response_dict.keys())
print("Total repositories:", response_dict['message'])
repo_dict = response_dict['data']
print("Repositories returned:", len(repo_dict))
