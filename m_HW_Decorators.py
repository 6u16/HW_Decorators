# Домашнее задание к лекции 3. «Decorators»

import os
from functools import wraps
import time

# 1.Логгер с посоянным путём для формирования log файла
def logger_1(old_function):
    
    @wraps(old_function)
    def new_function(*args, **kwargs):
        
        result =  old_function(*args, **kwargs)
                      
        file_path = os.path.join(os.getcwd(), 'data\main.log')  # строительство путик нашему файлу
        with open(file_path, 'a', encoding='utf-8') as f:  # вторым параметром указываем режим работы с файлом
            f.write(f'{time.ctime()}, name: {old_function.__name__}, args: {args}, kwargs: {kwargs}, result: {result}\n')
            
        return result
    
    return new_function


# 2.Логгер с переменным путём для формирования log файла
def logger_2(path):
    
    def __logger(old_function):
        def new_function(*args, **kwargs):
            
            result =  old_function(*args, **kwargs)
            
            file_path = os.path.join(os.getcwd(), path)  # строительство путик нашему файлу
            with open(file_path, 'a', encoding='utf-8') as f:  # вторым параметром указываем режим работы с файлом
                f.write(f'{time.ctime()}, name: {old_function.__name__}, args: {args}, kwargs: {kwargs}, result: {result}\n')
                
            return result
        
        return new_function

    return __logger


def test_1():

    path = 'data\main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_1
    def hello_world():
        return 'Hello World'

    @logger_1
    def summator(a, b=0):
        return a + b

    @logger_1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def test_2():
    
    paths = ('data\log_1.log', 'data\log_2.log', 'data\log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_2(path)
        def hello_world():
            return 'Hello World'

        @logger_2(path)
        def summator(a, b=0):
            return a + b

        @logger_2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

# 3.Применить написанный логгер к приложению
def test_3():
        
    path = 'data\log_gen.log'
    if os.path.exists(path):
        os.remove(path)
    
    @logger_2(path)
    # Генератор, для глубины вложенности списка = max_depth of python (возвращает список элементов подряд - плоское представление)
    def flat_generator_2(list_of_list):
        nested = True  # Условие входа в цикл while
        
        while nested:  # Цикл будет, пока есть хоть один элемент isinstance(i, list)
            new = []  # очищаем распакованный n-уровня список
            nested = False  # Разрешение выхода из while
            for i in list_of_list:  
                if isinstance(i, list):
                    new.extend(i)  # если да, то добавляем его в конец new extend-ом - так раскрываются скобки(вложения)
                    nested = True  # Запрет выхода из while
                else:
                    new.append(i)  # если нет, то просто добавляем элементы в new
            list_of_list = new  # Обновляем наш распакованный n-уровнем список для следующей итерации
        return list_of_list  # return в отличии от yield не присваивает функции тип = генератор
    
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    
    flat_generator_2(list_of_lists_2)

 
if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
