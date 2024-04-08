import requests
import json

url = "https://api.thenextleg.io/v2/imagine"

payload = json.dumps({
  "msg": "dog",
  "ref": "",
  "webhookOverride": "", 
  "ignorePrefilter": "false"
})
token = "" # nextleg's token
headers = {
  'Authorization': f'Bearer {token}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


