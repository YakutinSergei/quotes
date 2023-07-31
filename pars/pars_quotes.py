import requests
from bs4 import BeautifulSoup

from create_bot import bot
from data_base.quotes_db import quotes_add_bd

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
async def add_quotes(user_id):
    quotes_list = list ()
    urls = [['topic/motiviruyushhie', 16], ['friendship', 30], ['life', 30]]
    for ur in urls:
        for i in range(ur[1]):
            url = f"https://quote-citation.com/{ur[0]}/page/{i+1}"  # Замените ссылку на требуемую страницу
            # Отправляем GET запрос к странице
            response = requests.get(url=url, headers=headers)

            # Создаем объект BeautifulSoup для парсинга страницы
            soup = BeautifulSoup(response.text, "lxml")

            # Находим все ссылки на странице
            quotes = soup.find_all("div", class_='quote-text')
            # Выводим заголовок каждой ссылки
            for quote in quotes:
                quotes_list.append([quote.find("p").text, quote.find("p", class_='source').text])
            print(f'Страница № {i+1} обработана')

            #await quotes_add_bd(quote.find("p").text, quote.find("p", class_='source').text)
    await quotes_add_bd(quotes_list)

    await bot.send_message(chat_id=user_id, text='Парсинг завершен')

