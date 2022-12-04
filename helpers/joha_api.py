
import requests
import json
from lang import lang


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

    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)

    return json.loads(response.text)

# add_team_member("Jasur", "998909632147")
# {'error': True, 'message': 'Seller with given phone number is  exist'}

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

    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)

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
    # print( ans )
    return ans
    # {
    #     'order': {
    #         'id': 10, 
    #         'productOrderTime': '2022-11-29 17:35:21', 
    #         'productOrderCount': 8
    #     }, 
    #     'report': None, 
    #     'client': {
    #         'firstName': 'Jakhongirkhuja', 
    #         'lastName': 'Kholkhujaev', 
    #         'gender': 0, 
    #         'birthDate': '1989-03-28', 
    #         'language': 'ru', 
    #         'role': 'Creator', 
    #         'hrid': '2405671156440229', 
    #         'phonebook': {
    #             'id': 46, 
    #             'user_id': 68, 
    #             'phoneNumber': '998946121812', 
    #             'random': '327059', 
    #             'randomTime': '2022-10-11 20:47:19', 
    #             'status': 1, 
    #             'created_at': '2022-07-22T12:35:45.000000Z', 
    #             'updated_at': '2022-10-11T20:47:36.000000Z'
    #         }
    #     }, 
    #     'product': {
    #         'id': 5, 
    #         'store_id': 1, 
    #         'category_id': 1, 
    #         'productName': '{"ru": "TEST", "uz": "TEST"}',
    #         'productDescription': '{"ru": "test descripiont about product", "uz": "test descripiont about product"}', 
    #         'productIMG': 'a218bf94-491f-47a3-b441-56276e05a0a2-9DroukbH8nDGps2.jpg', 
    #         'productCost': 0,
    #         'productAmount': 100
    #     }
    # }

def sell_reports(product_id, seller_id, desc, filename, filetype, given):
    url = "https://api.pharmiq.uz/api/v1/bot/submitReport?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="
    payload={
        'product_code_id': str(product_id),
        'seller_id': str(seller_id),
        'shortDescription': desc,
        'action': str(given) # 0-reject 1-given
    }
    # print(payload)

    files={
        'reportIMG':  open( 'prooves/' + filename, 'rb' )
    }

    response = requests.post( url, data=payload, files=files, timeout=10)
    res = json.loads(response.text)
    # print(res)
    # {
    #     'store': {
    #         'product_code_id': '10', 
    #         'seller_id': '53', 
    #         'action': '1', 
    #         'shortDescription': 'Пропустить', 
    #         'reportIMG': 'bf0daf10-e64c-4236-9ebc-56534ddeb24a-aAFFIzgpPExZ2rv.png', 
    #         'updated_at': '2022-12-04T14:07:35.000000Z', 
    #         'created_at': '2022-12-04T14:07:35.000000Z', 
    #         'id': 5
    #     }, 
    #     'message': 'Store Seller Report has been Send'
    # }
    return res


def get_seller_id(phone):
    team = get_team()
    for member in team:
        if member["seller"]["sellerPhone"] == phone:
            return member["seller_id"]
    return 0


def gl(lang_str, json_dict):
    val = json.loads(json_dict)
    return val[lang_str]

def get_print_values(res:dict, lang:lang.ru):
    if( "error" in res and res["error"] == True ):
        return 1, "" # lang.prod_not_found
    text = f"""
{ lang.prod_name } : { gl( lang.abr, res["product"]["productName"] ) }
{ lang.prod_desc } : { gl( lang.abr, res["product"]["productDescription"] ) }
{ lang.client } : { res["client"]["firstName"] } { res["client"]["lastName"] }
{ lang.order_time } : { res["order"]["productOrderTime"] }
{ lang.phone } : { res["client"]["phonebook"]["phoneNumber"] }"""
    if( "report" in res and res["report"] and "action" in res["report"] and res["report"]["action"] ):
        return 2, text # lang.prod_sold
    return 0, text

if __name__ == "__main__":
    # print(del_team_member(4))
    # print( hash_check("ed0874b-3451-45d0-8aae-62e808ba8589") )
    print( add_team_member("Jasur", "998909632147") )


# {
#     'order': {
#         'id': 10, 
#         'productOrderTime': '2022-11-29 17:35:21', 
#         'productOrderCount': 8
#     }, 
#     'report': {
#         'id': 2, 
#         'product_code_id': 10, 
#         'seller_id': 53, 
#         'action': True, 
#         'reportIMG': 'b10be4cd-9de7-44c2-a8c4-10fec62bcbac-4dk3n2jrwL459Rd.png', 
#         'shortDescription': 'Skip', 
#         'dateTime': '2022-12-04 12:37:56', 
#         'created_at': '2022-12-04T12:37:55.000000Z', 
#         'updated_at': '2022-12-04T12:37:55.000000Z', 
#         'seller': {
#             'id': 53, 
#             'sellerName': 'Lazizjonov Jasurbek', 
#             'sellerPhone': '998946380341', 
#             'role': False, 
#             'created_at': '2022-12-03T16:41:57.000000Z', 
#             'updated_at': '2022-12-03T16:41:57.000000Z'
#         }
#     }, 
#     'client': {
#         'firstName': 'Jakhongirkhuja', 
#         'lastName': 'Kholkhujaev', 
#         'gender': 0, 
#         'birthDate': '1989-03-28', 
#         'language': 'ru', 
#         'role': 'Creator', 
#         'hrid': '2405671156440229', 
#         'phonebook': {
#             'id': 46, 
#             'user_id': 68, 
#             'phoneNumber': '998946121812', 
#             'random': '327059', 
#             'randomTime': '2022-10-11 20:47:19', 
#             'status': 1, 
#             'created_at': '2022-07-22T12:35:45.000000Z', 
#             'updated_at': '2022-10-11T20:47:36.000000Z'
#         }
#     }, 
#     'product': {
#         'id': 5, 
#         'store_id': 1, 
#         'category_id': 1, 
#         'productName': '{"ru": "TEST", "uz": "TEST"}', 
#         'productDescription': '{"ru": "test descripiont about product", "uz": "test descripiont about product"}', 
#         'productIMG': 'a218bf94-491f-47a3-b441-56276e05a0a2-9DroukbH8nDGps2.jpg', 
#         'productCost': 0, 
#         'productAmount': 100
#     }
# }