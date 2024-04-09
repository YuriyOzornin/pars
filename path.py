# sem4
# from lxml import html
# import requests

# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

# url = 'https://www.ebay.com'
# response = requests.get(url + '/b/Fishing-Equipment-Supplies/1492/bn_1851047', headers=header)
# dom = html.fromstring(response.text)

# items_list = []
# items = dom.xpath("//ul[@class='b-list__items_nofooter']li")
# for item in items:
#     item_info = {}

# name = item.xpath(".//h3[@class='s-item__title']/text()")
# link = item.xpath(".//h3[@class='s-item__title']/../href")
# price = item.xpath(".//span[@class='s-item__price']//text()")
# add_info = item.xpath(".//span[@class='NEGATIVE']/text()")

# item_info['name'] = name
# item_info['link'] = link
# item_info['price'] = price
# item_info['add_info'] = add_info
# items_list.append(item_info)

# print()

# hw4
import requests
from lxml import html
import csv
import pandas as pd
from fake_useragent import UserAgent 
import re
from urllib.parse import urljoin

url_base = "https://ru.wikipedia.org"
url = "https://ru.wikipedia.org/wiki/Список_городов_России_с_населением_более_100_тысяч_жителей"

ua = UserAgent() 
headers = {
    "User-Agent": ua.firefox, 
}

try:
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        print("Успешный запрос API по URL: ", response.url)
    else:
        print("Запрос API отклонен с кодом состояния:", response.status_code)

except requests.exceptions.RequestException as e:
    print("Ошибка в осущественнии HTML запроса:", e)

try:
    tree = html.fromstring(response.content)
    print(tree)
except html.etree.ParserError as e:
    print("Ошибка в парсинге HTML содержимого:", e)

try:
    table_rows = tree.xpath("//table[@class='wikitable sortable']/tbody/tr")
    len(table_rows)
    
except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)

try:
    years = table_rows[0].xpath("//th/span/text()")[2:]
    print(years)
    
except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)

years.insert(0, "Город")
years.append("Ссылка на информацию о городе")

df = pd.DataFrame(columns = years)
print(years)

# парсинг таблицы
try:
    for row in table_rows[2:]:
        # Работа с каждой ячейкой таблицы отдельно
        cells = row.xpath('.//td|.//th')[2:]
        
        # Если в ячейке таблицы значения нет, то возвращаем None 
        row_data = [cell.text_content().strip() if cell.text_content().strip() else None for cell in cells]
        
        # Если в ячейке таблицы прочерк, то замещаем его на None
        row_data = [None if item == '—' else item for item in row_data]
        
        # убираем референсные ссылки на источники статистических данных
        row_data = [re.sub("\[[0-9]+\]", '', s) if s is not None else None for s in row_data]
        
        # получаем ссылку на информацию о городе
        city_wiki_ref = urljoin(url_base, row.xpath(".//td//a/@href")[0])
        
        # Объединяем данные из строки в итоговую таблицу
        temp_df = pd.DataFrame(data = row_data)
        temp_df = temp_df.transpose()
        temp_df.columns = years[:-1]
        temp_df["Ссылка на информацию о городе"] = city_wiki_ref
        df = pd.concat([df, temp_df])
        #print(temp_df)
    
except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)

# Смотрим на готовую итоговую таблицу
df

df.to_csv('List of Russian cities population.csv', index=False)