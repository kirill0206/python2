
__author__ = 'ACV'

import os
import re
import csv
import json
import yaml
from chardet.universaldetector import UniversalDetector

'''
ex.1.  Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов 
    info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
  - Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание 
  данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров 
  «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить 
  в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, 
  os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить 
  в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
  Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
  - Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение 
  данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
  - Проверить работу программы через вызов функции write_to_csv().
'''

lesson_02_work_dir = 'lesson_02'
files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
parameters = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
output_files = ['main_data.txt', 'main_data.csv', 'main_data.json', 'main_data.yaml']

os.chdir(lesson_02_work_dir)


def get_encoding(file):
    detector = UniversalDetector()
    with open(file, 'rb') as text:
        for line in text:
            detector.feed(line)
            if detector.done:
                break
        detector.close()

    return detector.result['encoding']


def write_text(lst):
    with open(output_files[0], 'wb') as file:
        for row in lst:
            for item in row:
                file.write(item.encode())
            file.write('\n'.encode())


# extract parameters
data = list()
data.append(parameters)


def get_data():
    for file in files:
        with open(file, 'r', encoding=get_encoding(file)) as text:
            option = [None] * len(parameters)

            for line in text.readlines():
                for i in range(len(parameters)):
                    if re.match(parameters[i], line):
                        option[i] = line[len(parameters[i])+1:].strip()
                #print(option)
                if None not in option:
                    break
            data.append(option)

    write_text(data)


def write_to_csv(csv_file_path):
    get_data()
    with open(csv_file_path, 'w') as file:
        file_writer = csv.writer(file)
        for row in data:
            file_writer.writerow(row)


def read_from_csv(csv_file_path):
    read_data = list()
    with open(csv_file_path, 'r') as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            read_data.append(row)

    return read_data


write_to_csv(output_files[1])


'''
ex.2.  Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать 
скрипт, автоматизирующий его заполнение данными. Для этого:
  - Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), 
  цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл 
  orders.json. При записи данных указать величину отступа в 4 пробельных символа;
  - Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
        }

    with open(output_files[2], 'w') as file:
        json.dump(dict_to_json, file, indent=4)


write_order_to_json('15235', 5, 5005.15, 'HarryPotter', '17121998')


def write_to_json(file, w_data):
    with open(file, 'w') as file:
        json.dump(w_data, file, indent=4, ensure_ascii=False)


def read_from_json(file):
    with open(file, 'r') as xfile:
        r_data = json.load(xfile)
    return r_data

'''
ex.3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. 
Для этого:
  - Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, 
  третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим 
  в кодировке ASCII (например, €);
  - Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию 
  файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
  - Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

dict_to_yaml = {
    'key_1': ['Still', 'waters', 'run', 'deep'],
    'key_2': 1,
    'key_3': {'price_1': '11€',
              'price_2': '13$',
              'price_3': '700₽',
              }
    }


def write_to_yaml(file_path, w_data):
    with open(file_path, 'w') as file:
        yaml.dump(w_data, file, default_flow_style=False, allow_unicode=True)


def read_from_yaml(file_path):
    with open(file_path, 'r') as file:
        file_content = yaml.load(file, Loader=yaml.Loader)
    return file_content


write_to_yaml(output_files[3], dict_to_yaml)
dict_from_yaml = read_from_yaml(output_files[3])

if dict_to_yaml == dict_from_yaml:
    print('Dict writing to yaml-file and reading are equal')

'''
ex.add
Реализовать скрипт для преобразования данных в формате csv в формат json;
Реализовать скрипт для преобразования данных в формате csv в формат yaml;
Реализовать скрипт для преобразования данных в формате json в формат yaml.
'''


def from_csv_to_json():
    csv_to_json_data = read_from_csv(output_files[1])
    write_to_json('csv_to_json.json', csv_to_json_data)


def from_csv_to_yaml():
    csv_to_yaml_data = read_from_csv(output_files[1])
    write_to_yaml('csv_to_yaml.yaml', csv_to_yaml_data)


def from_json_to_yaml():
    json_to_yaml_data = read_from_json('csv_to_json.json')
    print(json_to_yaml_data)
    write_to_yaml('json_to_yaml.yaml', json_to_yaml_data)


from_json_to_yaml()
