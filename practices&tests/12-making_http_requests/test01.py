import requests as rq

url = 'https://icanhazdadjoke.com/'

response = rq.get(url, headers={'accept': 'application/json'})
data = response.json()

print(type(data))
print(data['joke'])
print(data['status'])