# coding=utf-8
from students.management.commands.tests import Type

questions = [
    {
        'question': 'Какие из этих не является языком программирования?',
        'type': Type.Multiple,
        'answers': [
            'Python',
            '##HTML',
            '##CSS',
            'JS'
        ]
    },
    {
        'question': 'Выберите все правильные строки в Python?',
        'type': Type.Multiple,
        'answers': [
            '##"Это строка"',
            '##\'И это тоже строка!\'',
            '##u"А это ведь не строка"',
            '##u\'Может это не строка?\''
        ]
    },
    {
        'question': 'Какого типа не существует в языке Python?',
        'type': Type.Single,
        'answers': [
            'int',
            '##char',
            'str',
            'bool'
        ]
    },
    {
        'question': '[Python] Каким будет результат выражения <div class="code">2**4</div>?',
        'type': Type.Single,
        'answers': [
            '8',
            '##16',
            '32',
            '64'
        ]
    },
    {
        'question': '[Python] Как создается пустой список?',
        'type': Type.Single,
        'answers': [
            '##[]',
            '()',
            '{}',
            '{()}'
        ]
    },
    {
        'question': '[Python] Что делает функция range()?',
        'type': Type.Single,
        'answers': [
            'Цикл от 0 до указанного числа',
            'Цикл от 1 до указанного числа',
            '##Создает список от 0 до указанного числа',
            'Проверяет длину списка'
        ]
    },
    {
        'question': '[Python] Как перебрать все элементы списка array?',
        'type': Type.Single,
        'answers': [
            '##for item in array:',
            'for(int i;i<array.size();i++)',
            'foreach(array)',
            'for i in range(array):'
        ]
    },
    {
        'question': '[Python] Что такое словарь(map)?',
        'type': Type.Multiple,
        'answers': [
            '##Структура данных в котором значения хранятся по ключу',
            '##Структура данных в котором каждому ключу соответствует одно значение',
            'Книжка в котором можно найти английские переводы',
            'Книжка в котором можно найти русско-кыргызские переводы'
        ]
    },
    {
        'question': '[Python] Как указать что функция ничего не возвращает?',
        'type': Type.Single,
        'answers': [
            'написать void в начале',
            'return None в конце',
            '##такое невозможно сделать',
            'функции и так ничего не возвращают'
        ]
    },
    {
        'question': '[Python] Какое ключевое слово указывается при создании функции?',
        'type': Type.Single,
        'answers': [
            '##def',
            'function',
            'public',
            'func'
        ]
    },
    {
        'question': '[Python] Чем отделяются внутренние и внешние блоки кода?',
        'type': Type.Single,
        'answers': [
            'фигурными скобками {}',
            '##отступами',
            'begin end',
            'круглыми скобками ()'
        ]
    },
    {
        'question': '[Python] Как взять последний элемент списка array?',
        'type': Type.Single,
        'answers': [
            '##array[-1]',
            'array[0]',
            'array.last()',
            'array[-0]'
        ]
    },
    {
        'question': '[Python] Как вывести на экран значение?',
        'type': Type.Single,
        'answers': [
            '##print()',
            'System.out.println()',
            'console.log()',
            'write()'
        ]
    },
    {
        'question': '[Python] Как подключить функцию factorial() из файла math.py?',
        'type': Type.Single,
        'answers': [
            '##from math import factorial',
            'import math.factorial()',
            'import math from factorial',
            'podkluchit\' math.factorial'
        ]
    },
    {
        'question': '[Python] Как прочитать с экрана то, что ввел пользователь?',
        'type': Type.Single,
        'answers': [
            '##с помощью метода input() или raw_input()',
            'я не помню',
            'readln()',
            'from screen import text'
        ]
    },
    {
        'question': '[Python] Что выведется на экран<br><div class="code">'
                    'd = 10<br>'
                    'if d >= 11:<br>'
                    '<div class="tab"></div>print "salut"<br>'
                    'else:<br>'
                    '<div class="tab"></div>print "aloha"'
                    '</div>?',
        'type': Type.Single,
        'answers': [
            'salut',
            '##aloha',
            'salut и aloha',
            'ничего'
        ]
    },
    {
        'question': '[Python] Как объявить функцию с двумя параметрами?',
        'type': Type.Single,
        'answers': [
            'def func(2 params):',
            'def func(2):',
            'def func[2]:',
            '##def func(param, param2):'
        ]
    },
    {
        'question': '[Python] Что такое классы?',
        'type': Type.Single,
        'answers': [
            '##Абстрактное описание реальных сущностей с помощью языка программирования',
            'Возрастные уровни в школе',
            '**Из них можно создать объекты',
            'Да какая разница, все равно не сдам'
        ]
    },
    {
        'question': '[Python] Как создать объект класса Dog?',
        'type': Type.Single,
        'answers': [
            '##dog = Dog()',
            'Dog() = d',
            'd = Dog',
            'dog = new Dog()'
        ]
    },
    {
        'question': '[Python] Что такое self в методах класса?',
        'type': Type.Single,
        'answers': [
            '##Ссылка на текущий объект',
            'Указатель на класс',
            'Первый параметр',
            'Свойство класса'
        ]
    },
]
