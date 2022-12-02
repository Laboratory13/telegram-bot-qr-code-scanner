
import requests
import json


headers = {
    "Content-Type": "multipart/form-data",
    "Content-Type": "application/x-www-form-urlencoded",
    'Accept': 'application/json',
}

def add_team_member(name, phone):
    url = "https://api.pharmiq.uz/api/v1/bot/myteam/add?hrid=1034418716553026&token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="
    
    payload={
        'sellerName': name,
        'sellerPhone': phone,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

# add_team_member("Jasur", "998909632147")

def get_team():
    url = "https://api.pharmiq.uz/api/v1/bot/myteam?hrid=1034418716553026&token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)

def del_team_member(id):
    url = "https://api.pharmiq.uz/api/v1/bot/myteam/delete/4?hrid=1034418716553026&token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

    payload={
        'id': id,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def register():
    url = "https://api.pharmiq.uz/api/v1/bot/register?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

    payload={
        'sellerPhone': '998946667788',
        'telegram_id': '22323232',
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def hash_check(hash_code):
    url = "https://api.pharmiq.uz/api/v1/bot/checkHash?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

    payload={
        'hash': hash_code,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def sell_reports(product_id, seller_id, desc, filename, filetype, given):
    url = "https://api.pharmiq.uz/api/v1/bot/submitReport?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="

    payload={
        'product_code_id': str(product_id),
        'seller_id': str(seller_id),
        'shortDescription': desc,
        'action': given
    }
    files=[
        (
            'reportIMG',
            (
                filename, # '800px-Sign-check-icon.png',
                open( 'prooves/' + filename, 'rb' ),
                filetype # 'image/png'
            )
        )
    ]

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)

if __name__ == "__main__":
    print(del_team_member())