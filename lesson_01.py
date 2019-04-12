
__author__ = 'ACV'


import os
from chardet.universaldetector import UniversalDetector

'''
ex. 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
'''

word_11 = 'разработка'
word_12 = 'сокет'
word_13 = 'декоратор'

print(type(word_11), word_11)
print(type(word_12), word_12)
print(type(word_13), word_13)


'''
ex. 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
'''

word_21 = b'class'
word_22 = b'function'
word_23 = b'method'

print(type(word_21), word_21, len(word_21))
print(type(word_22), word_22, len(word_22))
print(type(word_23), word_23, len(word_23))


'''
ex. 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''

word_31 = b'attribute'
#word_32 = b'класс'
#word_33 = b'функция'
word_34 = b'type'


'''
ex. 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
'''

word_41 = 'разработка'
word_42 = 'администрирование'
word_43 = 'protocol'
word_44 = 'standard'

word_41 = word_41.encode()
word_42 = word_42.encode()
word_43 = word_43.encode()
word_44 = word_44.encode()

print(word_41)
print(word_42)
print(word_43)
print(word_44)

word_41 = word_41.decode()
word_42 = word_42.decode()
word_43 = word_43.decode()
word_44 = word_44.decode()

print(word_41)
print(word_42)
print(word_43)
print(word_44)


'''
ex. 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
на кириллице.
'''


'''
ex. 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

os.chdir('lesson_01')
with open('test_file.txt', 'w') as file:
    file.write('сетевое программирование\n')
    file.write('сокет\n')
    file.write('декоратор\n')

detector = UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for line in file:
        detector.feed(line)
        if detector.done:
            break
    detector.close()

print('Кодировка файла {}'.format(detector.result['encoding']))

with open('test_file.txt', 'r', encoding='utf-8') as file:
    print(file.read())
