import json
import requests
from bs4 import BeautifulSoup

def get_pet_values():
    print("Подключаемся к сайту Guide Builder...")
    url = "https://guide-builder.ru/adopt-me-calculator-valut-trade/"
    
    # Маскируемся под обычный браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Ищем тот самый тег script с атрибутом data-gb-mm2-trade-data
            data_script = soup.find('script', attrs={'data-gb-mm2-trade-data': True})
            
            if data_script and data_script.string:
                # 2. Превращаем текст внутри скрипта в удобный формат Python (словарь/список)
                raw_data = json.loads(data_script.string)
                clean_db = {}
                
                # 3. Перебираем каждый предмет из полученной базы
                for item in raw_data:
                    name = item.get('name')
                    # Забираем базовое значение (value) из JSON
                    value = item.get('value', 0) 
                    
                    if name:
                        clean_db[name] = value
                        
                return clean_db
            else:
                print("Ошибка: Не удалось найти JSON-данные на странице.")
                return None
        else:
            print(f"Ошибка доступа к сайту: Код {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при парсинге: {e}")
        return None

def save_to_json(data, filename="prices.json"):
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            # Сохраняем в файл. indent=4 делает его красивым и читаемым
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Успех! Сохранено {len(data)} питомцев/предметов в {filename}")
    else:
        print("Данных нет, файл не обновлен.")

if __name__ == "__main__":
    pet_prices = get_pet_values()
    save_to_json(pet_prices)
