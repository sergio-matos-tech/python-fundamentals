import requests

response = requests.get('https://ge.globo.com/')


print(response)
print(response.ok)
print(response.headers)
# print(response.text)