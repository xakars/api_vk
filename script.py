import requests
import random
import os
from useful_tools import save_image
from dotenv import load_dotenv


def fetch_image_from_xkcd():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_post = response.json()["num"]
    random_post = random.randrange(total_post)
    url = f"https://xkcd.com/{random_post}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    img_url = response_json["img"]
    filename = f"{response_json['safe_title']}{'.png'}"
    comment = response_json["alt"]
    save_image(img_url, filename)
    return filename, comment


def get_server_address_for_upload(token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload = {
        "access_token": token,
        "v": 5.131,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_photo_to_server(token, photo_name):
    with open(photo_name, 'rb') as file:
        url = get_server_address_for_upload(token)
        payloads = {
            "access_token": token,
            "v": 5.131
        }
        files = {
            'photo': file
        }
        response = requests.post(url, params=payloads, files=files)
    response.raise_for_status()
    response_json = response.json()
    vk_server = response_json["server"]
    vk_photo = response_json["photo"]
    vk_hash = response_json["hash"]
    return vk_server, vk_photo, vk_hash


def save_uploaded_photo(token, photo_name):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    vk_server, vk_photo, vk_hash = upload_photo_to_server(token, photo_name)
    payloads = {
        "access_token": token,
        "v": 5.131,
        "server": vk_server,
        "hash": vk_hash,
    }
    vk_data = {
        "photo": vk_photo
    }
    response = requests.post(url, params=payloads, data=vk_data)
    response.raise_for_status()
    response_json = response.json()["response"]
    media_id = response_json[0]["id"]
    owner_id = response_json[0]["owner_id"]
    return owner_id, media_id


def post_photo_to_wall(token, group_id, photo_name, message):
    url = "https://api.vk.com/method/wall.post"
    owner_id, media_id = save_uploaded_photo(token, photo_name)
    payloads = {
        "access_token": token,
        "v": 5.131,
        "from_group": 1,
        "message": message,
        "owner_id": -int(group_id),
        "attachments": f"photo{owner_id}_{media_id}>"
    }
    response = requests.post(url, params=payloads)
    response.raise_for_status()


def main():
    load_dotenv()
    token = os.environ["ACCESS_TOKEN"]
    group_id = os.environ["GROUP_ID"]
    photo_name, message = fetch_image_from_xkcd()
    post_photo_to_wall(token, group_id, photo_name, message)
    os.remove(photo_name)

if __name__ == "__main__":
    main()
