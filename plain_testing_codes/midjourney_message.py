import requests
import json

url = "https://api.thenextleg.io/v2/message/zE48JgcE0FJOjJMc0khX?expireMins=2"

headers = {
  'Authorization': 'Bearer 054f5451-1b6e-4626-9d0f-30fc503375ba',
}
response = requests.request("GET", url, headers=headers)

print(response.text)
                
