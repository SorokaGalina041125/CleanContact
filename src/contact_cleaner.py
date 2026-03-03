import csv
import re
import os
from pprint import pprint

# Получаем пути к файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "phonebook_raw.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "phonebook.csv")

print(f"📂 Читаем файл: {INPUT_FILE}")
print("=" * 60)

# читаем адресную книгу в формате CSV в список contacts_list
with open(INPUT_FILE, encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Сохраняем заголовки
headers = contacts_list[0]
contacts = contacts_list[1:]

print(f"📊 Исходных записей: {len(contacts)}")
print("=" * 60)

# TODO 1: Приводим ФИО в правильный формат
for contact in contacts:
    # Объединяем первые три поля в одну строку и разбиваем по пробелам
    full_name = ' '.join(contact[:3]).split()
    
    # Заполняем поля в зависимости от количества слов
    if len(full_name) >= 3:
        contact[0] = full_name[0]  # фамилия
        contact[1] = full_name[1]  # имя
        contact[2] = full_name[2] if len(full_name) > 2 else ''  # отчество
    elif len(full_name) == 2:
        contact[0] = full_name[0]  # фамилия
        contact[1] = full_name[1]  # имя
        contact[2] = ''              # отчество пустое
    elif len(full_name) == 1:
        contact[0] = full_name[0]  # фамилия
        contact[1] = ''              # имя пустое
        contact[2] = ''              # отчество пустое

# TODO 2: Приводим телефоны к нужному формату
phone_pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})'
extension_pattern = r'[\(]?доб\.?\s*(\d+)[\)]?'

for contact in contacts:
    phone = contact[5]
    if phone:
        # Ищем добавочный номер
        extension = re.search(extension_pattern, phone)
        
        # Форматируем основной номер
        formatted_phone = re.sub(phone_pattern, r'+7(\2)\3-\4-\5', phone)
        
        # Убираем лишние символы из результата
        formatted_phone = re.sub(r'\s*[\(]?доб\.?\s*\d+[\)]?\s*', '', formatted_phone)
        
        # Добавляем добавочный номер, если он был
        if extension:
            formatted_phone += f' доб.{extension.group(1)}'
        
        contact[5] = formatted_phone

# TODO 3: Объединяем дубликаты
unique_contacts = {}
for contact in contacts:
    # Ключ - фамилия + имя (приводим к нижнему регистру для надежности)
    key = (contact[0].lower(), contact[1].lower())
    
    if key not in unique_contacts:
        unique_contacts[key] = contact
    else:
        existing = unique_contacts[key]
        for i in range(len(contact)):
            # Если поле пустое, а в новом контакте есть данные - заполняем
            if existing[i] == '' and contact[i] != '':
                existing[i] = contact[i]
            # Для телефона и email если разные - объединяем через запятую
            elif i in [5, 6] and existing[i] != '' and contact[i] != '' and existing[i] != contact[i]:
                existing[i] = f"{existing[i]}, {contact[i]}"

# Формируем финальный список с заголовками
result_contacts = [headers] + list(unique_contacts.values())

print("📋 ИСХОДНЫЕ ДАННЫЕ (phonebook_raw.csv):")
print("-" * 60)
for i, contact in enumerate(contacts_list):
    print(f"{i:2}. {contact}")
print("=" * 60)

print("\n📋 ОБРАБОТАННЫЕ ДАННЫЕ (после нормализации):")
print("-" * 60)
for i, contact in enumerate(contacts):
    print(f"{i:2}. {contact}")
print("=" * 60)

print("\n📋 УНИКАЛЬНЫЕ ЗАПИСИ (после удаления дубликатов):")
print("-" * 60)
for i, contact in enumerate(result_contacts[1:], 1):
    print(f"{i:2}. {contact}")
print("=" * 60)

print(f"\n💾 Сохраняем результат в: {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_contacts)

print(f"✅ Готово! Данные очищены и сохранены")
print(f"📊 Было записей: {len(contacts_list)-1}, стало: {len(result_contacts)-1}")
print(f"📁 Файл сохранен: {OUTPUT_FILE}")