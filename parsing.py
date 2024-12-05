import requests
from lxml import html
import csv

# Создадим код, который позволит совершать парсинг таблицы Википедии для отслеживания популяции населения стран
# URL страницы с таблицей населения
url = 'https://ru.wikipedia.org/wiki/Список_государств_и_зависимых_территорий_по_населению'

# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

try:
    # Отправка GET-запроса для получения HTML-контента страницы.
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на ошибки запроса

    # Парсинг HTML-содержимого
    tree = html.fromstring(response.content)

    # XPath выражение для выбора строк таблицы
    rows = tree.xpath('//table[@class="standard sortable"]/tbody/tr')

    # Список для хранения данных
    data = []

    # Извлечение данных из строк таблицы
    for row in rows[1:]:  # Единица, т.к. пропускаем заголовок таблицы
        try:
            # Извлечение данных из ячеек. Функция strip позволяет игнорировать пробелы в тексте
            rank = row.xpath('./td[1]/text()')[0].strip() # [0] нужна для вызова строки 'text', а не списка ['text']
            country = row.xpath('./td[2]//text()')  # Извлечение текста с учетом вложенных элементов
            country = ''.join(country).strip()  # Объединяем список строк в одну
            population = row.xpath('./td[3]/text()')[0].strip()
            date = row.xpath('./td[4]/text()')[0].strip()
            percentage = row.xpath('./td[5]/text()')[0].strip()
            source = row.xpath('./td[6]//text()')  # Извлечение текста с учетом вложенных элементов
            source = ''.join(source).strip()

            # Добавление данных в список по столбцам
            data.append([rank, country, population, date, percentage, source])
        except IndexError:
            print("Ошибка при извлечении данных из строки, пропускаем строку.")

    # Сохранение данных в CSV-файл
    with open('population_data.csv', mode='w', newline='', encoding='utf-8') as file: #'w' означает "write" (запись). Установка newline='' позволяет избежать проблем с добавлением лишних пустых строк при записи в файл
        writer = csv.writer(file)
        # Запись заголовков
        writer.writerow(['№', 'Страна', 'Население', 'Дата', '% от населения Земли', 'Источник'])
        # Запись данных
        writer.writerows(data)

    print("Данные успешно извлечены и сохранены в 'population_data.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")

