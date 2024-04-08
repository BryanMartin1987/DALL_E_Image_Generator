import requests
import json

url = "https://api.thenextleg.io/v2/message/zE48JgcE0FJOjJMc0khX?expireMins=2"

headers = {
  'Authorization': 'Bearer ', # put token here as well
}
response = requests.request("GET", url, headers=headers)

print(response.text)
                
