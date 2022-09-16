# api_vk

Скрипт предназначен для публикации комиксов в группу в социальной сети [ВКонтакте](https://vk.com/). Комиксы берутся рандомно из сайта [xkcd.com](https://xkcd.com/)

Команда для установки зависимостей:
``` 
pip install -r requirements.txt
``` 
Чтобы пользоваться скрипотом Вам понадобится токен access_token для [ВКонтакте](https://vk.com/).

Задайте ACCESS_TOKEN в файле .env, а также id группы в параметре GROUP_ID:
```
ACCESS_TOKEN=
GROUP_ID=
```
Запустите скрипт командой:
```
python script.py
```