import requests


def save_image(url, file_name):
    response = requests.get(url)
    extension = ".png"
    file_name = f"{file_name}"
    with open(file_name, "wb") as file:
        file.write(response.content)
