
import requests
import json

url = "https://api.pharmiq.uz/api/v1/bot/myteam/add?hrid=1034418716553026&token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

def team_add(name, phone):
    payload={
        'sellerName': name,
        'sellerPhone': phone,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }
    files=[

    ]
    headers = {
        "Content-Type": "multipart/form-data",
        "Content-Type": "application/x-www-form-urlencoded",
        'Accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

team_add("Jasur", "998909632147")

# {
#     "error":true,
#     "message":{
#         "platform":["validation.required"],
#         "device":["validation.required"],
#         "browser":["validation.required"],
#         "timeZone":["validation.required"]
#     }
# }