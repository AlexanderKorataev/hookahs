import requests
import json

# Загрузка данных из JSON файла
with open('response_1712132463459.json', 'r') as file:
    data = json.load(file)

# URL эндпоинта
url = 'https://bus-tracker.ru/api/v1/statistics/data/'

# Цикл для отправки каждого элемента из JSON
for item in data:
    # Отправка POST запроса на эндпоинт

    item.pop('id', None)

    # Заменяем 'owner_id' на 'floating_id'
    item['floating_id'] = item.pop('owner_id', None)
    
    # print(item)
    # exit()
    
    response = requests.post(
                url,
                params={
                    'id_': item['id_'],
                    'datetime': item['disappearance_time'],
                    'floating_id': item['floating_id']
                },
                verify=False
            )
    
    # Проверка успешности запроса
    if response.status_code == 200:
        print(f'Data for id {item["id_"]} sent successfully.')
    else:
        print(f'Failed to send data for id {item["id_"]}.')

