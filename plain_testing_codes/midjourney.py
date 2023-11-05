import requests
import json

url = "https://api.thenextleg.io/v2/imagine"

payload = json.dumps({
  "msg": "dog",
  "ref": "",
  "webhookOverride": "", 
  "ignorePrefilter": "false"
})
headers = {
  'Authorization': 'Bearer 054f5451-1b6e-4626-9d0f-30fc503375ba',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


