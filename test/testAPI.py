import requests

url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
s= requests.get(url)
print(s.status_code)

