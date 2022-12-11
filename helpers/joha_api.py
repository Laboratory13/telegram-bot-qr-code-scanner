
import requests
import json
from lang import lang


headers = {
    "Content-Type": "multipart/form-data",
    "Content-Type": "application/x-www-form-urlencoded",
    'Accept': 'application/json',
}

def add_team_member(hrid, name, phone):
    url = "https://api.pharmiq.uz/api/v1/bot/myteam/add"
    params={
        'hrid' : str(hrid),
        'token' : 'dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q='
    }
    payload={
        'sellerName': name,
        'sellerPhone': phone,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }
    response = requests.request("POST", url, params=params, data=payload, timeout=10)
    return json.loads(response.text)



def get_team( hrid ):
    url = "https://api.pharmiq.uz/api/v1/bot/myteam"
    params={
        'hrid' : str(hrid),
        'token' : 'dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q='
    }
    response = requests.request("GET", url, params=params)
    return json.loads(response.text)



def del_team_member(hrid, id):
    url = "https://api.pharmiq.uz/api/v1/bot/myteam/delete/" + id
    params={
        'hrid' : str(hrid),
        'token' : 'dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q='
    }
    payload={
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }
    response = requests.request("POST", url, params=params, data=payload, timeout=10)
    return json.loads(response.text)



def register(phone, tg_id):
    url = "https://api.pharmiq.uz/api/v1/bot/register?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="
    payload={
        'sellerPhone': phone,
        'telegram_id': tg_id,
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
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
    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    ans = json.loads(response.text)
    return ans


def sell_reports(product_id, seller_id, desc, filename, filetype, given):
    url = "https://api.pharmiq.uz/api/v1/bot/submitReport?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="
    payload={
        'product_code_id': str(product_id),
        'seller_id': str(seller_id),
        'shortDescription': desc,
        'action': str(given) # 0-reject 1-given
    }
    files={
        'reportIMG':  open( 'prooved/' + filename, 'rb' )
    }
    response = requests.post( url, data=payload, files=files, timeout=10)
    res = json.loads(response.text)
    return res


def gl(lang_str, json_dict):
    val = json.loads(json_dict)
    return val[lang_str]

def get_print_values(res:dict, lang:lang.ru):
    if( "error" in res or "product" not in res or res["product"] == None or "client" not in res or res["client"] == None ):
        return 1, "" # lang.prod_not_found
    try:
        arr = [
            f'{ lang.prod_name } : { gl( lang.abr, res["product"]["productName"] ) }', 
            f'{ lang.prod_desc } : { gl( lang.abr, res["product"]["productDescription"] ) }',
            f'{ lang.client } : { res["client"]["firstName"] } { res["client"]["lastName"] }',
            f'{ lang.order_time } : { res["order"]["productOrderTime"] }',
            f'{ lang.phone } : { res["client"]["phonebook"]["phoneNumber"] }',
        ]
        text = '\n'.join(str(x) for x in arr)
        if( "report" in res and res["report"] and "action" in res["report"] and res["report"]["action"] ):
            return 2, text # lang.prod_sold
        return 0, text
    except:
        return 1, "" # lang.prod_not_found
