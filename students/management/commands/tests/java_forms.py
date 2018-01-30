# coding=utf-8
from students.management.commands.tests import Type

questions = [
    {
        'question': 'От какого класса нужно унаследовать, чтобы создать форму на Java?',
        'type': Type.Single,
        'answers': [
            '##JFrame',
            'IFrame',
            'JPanel',
            'JForm',
        ]
    },
    {
        'question': 'Как установить основной контейнер окна?',
        'type': Type.Single,
        'answers': [
            'setMainContainer()',
            '##setContentPane()',
            'setMainPanel()',
            'yaNeznayuOtveta()',
        ]
    },
    {
        'question': 'Внутри какого метода контейнеров выполняется отрисовка?',
        'type': Type.Single,
        'answers': [
            'draw()',
            'otrisovka()',
            '##paint()',
            'photoshop()',
        ]
    },
    {
        'question': 'Через объект какого класса происходит отрисовка в контейнерах?',
        'type': Type.Single,
        'answers': [
            'Canvas',
            '##Graphics',
            'Object',
            'Paint',
        ]
    },
    {
        'question': 'Какие методы есть у класса Graphics?',
        'type': Type.Multiple,
        'answers': [
            '##drawOval()',
            '##drawLine()',
            '##drawRect()',
            'drawKvadrat()',
        ]
    },
    {
        'question': 'Какой метод нужно вызвать чтобы перерисовать контейнер?',
        'type': Type.Single,
        'answers': [
            'redraw()',
            '##repaint()',
            'container()',
            'peredraw()',
        ]
    },
    {
        'question': 'Как установить размер окна в 300px ширину и в 200px в высоту?',
        'type': Type.Single,
        'answers': [
            '##setSize(300, 200)',
            'setBounds(300, 200)',
            'setBounds(200, 300)',
            'setSize(200, 300)',
        ]
    },
    {
        'question': 'Тут еще один умный вопрос?',
        'type': Type.Single,
        'answers': [
            '**Этот ответ типа правильный',
            '**Это точно неправильный',
            '**Это непонятный ответ',
        ]
    },
    {
        'question': 'От какого класса нужно наследовать чтобы создать тесты?',
        'type': Type.Single,
        'answers': [
            '##TestCase',
            'Test',
            'CreateTest',
            'TestMest',
        ]
    },
    {
        'question': 'Какое необходимое условие для методов тестовых классов?',
        'type': Type.Multiple,
        'answers': [
            '##Начинаться со слова test',
            'Заканчиваться со словом test',
            'Содержать слово test',
            '**Называться понятно',
        ]
    },
    {
        'question': 'Какие методы проверяют правильность в тестах?',
        'type': Type.Multiple,
        'answers': [
            '##assertEquals()',
            '##assertNull()',
            '##assertTrue()',
            '##assertFalse()',
        ]
    }
]