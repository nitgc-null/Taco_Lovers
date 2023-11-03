import datetime
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
project_id = os.getenv("PROJECT_ID")
referer_domain = os.getenv("REFERER_DOMAIN")
collection_name = os.getenv("COLLECTION_NAME")

def anonymous_login():
    response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}',
                             headers={'Content-Type': 'application/json',
                                      'Referer': referer_domain},
                             data=json.dumps({}))

    if response.status_code == 200:
        id_token = response.json()['idToken']
        uid = response.json()['localId']  # This is the user's UID
        print("正常に匿名ログインができましたわ。")
        print("こちらがUIDですわ:", uid)
        return id_token, uid
    else:
        print('正常に匿名ログインができませんでしたわ。\n以下がエラー内容になりますわ。\n', response.content)
        return None, None

def love_tacos(collection_id, document_id, token):
    url = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_id}/{document_id}?key={api_key}'
    data = {
        'fields': {
            'time': {
                'timestampValue': datetime.datetime.now().isoformat() + 'Z'
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print('正常にいいね🤍をしましたわ。')
    else:
        print('正常にいいね🤍ができませんでしたわ。\n以下がエラー内容になりますわ。\n', response.content)

def count_tacos_lovers(collection_id, token):
    url = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_id}?key={api_key}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    documents = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page = response.json()
            documents.extend(page.get('documents', []))
            url = page.get('nextPageToken')
            if url:
                url = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_id}?key={api_key}&pageToken={url}'
        else:
            print('いいね数を取得できませんでしたわ。\n以下がエラー内容になりますわ。\n', response.content)
            return None
    print(f'現在のいいねは{len(documents)}いいねですわ🌮🔥')
    return documents

def main():
    print("""
+======================================================+
| _________  _________    __   ____ _   _________  ____|
|/_  __/ _ |/ ___/ __ \  / /  / __ \ | / / __/ _ \/ __/|
| / / / __ / /__/ /_/ / / /__/ /_/ / |/ / _// , _/\ \  |
|/_/ /_/ |_\___/\____/ /____/\____/|___/___/_/|_/___/  |
+======================================================+
""")
    num_times = int(input("いいね🤍する回数を入力してくださいまし。\n"))
    for _ in range(num_times):
        token, uid = anonymous_login()
        if uid is not None:
            love_tacos(collection_name, uid, token)
    count_tacos_lovers(collection_name, token)
    input("いいね🤍の処理がすべて完了しましたわ。\n何かキーを押して終了してくださいまし。")

if __name__ == "__main__":
    main()
