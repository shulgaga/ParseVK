# VK-parsing Bot
VK-parsing Bot - это телеграм-бот для поиска объявлений с подпиской на категории нужных товаров.
Пользователь вводит название категории, к примеру "машины", после вводит название марки, к примеру "BMW".
И получает ответ в виде 30-ти объявлений.

<img src= "" width = "100" height = "100" > 

Попробовать: https://t.me/Avito_animals_bot

## Дополнительная документация:



Проект Django запущен на ngork, используется база данных Sqlite3.

## Сборка репозитория и локальный запуск
Выполните в консоли:
```
git clone https://github.com/shulgaga/ParseVK.git
pip install -r requirments.txt
```
 
### Настройка
Создайте файл .env и добавьте туда следующие настройки:
```
BOT_API_KEY = "Апи ключ, который вы получили у BotFather"
API_TOKEN_VK = "Сервисный ключ доступа VK_API"
ACCESS_TOKEN_VK = "Ключ доступа пользователя VK_API"
VERSION = "5.131" - последняя версия VK_API

METHOD_WALL_SEARCH = "https://api.vk.com/method/wall.search"
```

### Запуск
Чтобы запустить бота и django-server, выполните в консоли:
```
python manage.py runserver
python manage.py bot
```