# coding=utf-8
from students.management.commands.tests import Type

questions = [
    {
        'question': 'Зачем нужен pip?',
        'type': Type.Single,
        'answers': [
            'Чтобы импортировать библиотеки в программу',
            '##Чтобы скачивать другие библиотеки',
            'Без него python не заработает',
            'Чтобы в консоли можно было запускать код python'
        ]
    },
    {
        'question': 'Зачем нужен virtualenv?',
        'type': Type.Single,
        'answers': [
            '##Чтобы для каждого проекта были свои библиотеки',
            'Чтобы устанавливать другие библиотеки',
            'Без него python не заработает',
            'Чтобы в консоли можно было запускать код python'
        ]
    },
    {
        'question': 'Django - это',
        'type': Type.Single,
        'answers': [
            '##Фреймворк для веб разработки',
            'Библиотека для HTML, CSS и JS',
            'Помогает не писать лишний HTML код',
            'Помощник для работы с БД'
        ]
    },
    {
        'question': '[Django] Где указывается что главная страница должна обрабатываться классом HomeView?',
        'type': Type.Single,
        'answers': [
            'settings.py',
            '##urls.py',
            'models.py',
            'views.py'
        ]
    },
    {
        'question': '[Django] Что такое urls.py?',
        'type': Type.Single,
        'answers': [
            'это файл в котором есть обработчики ссылок',
            '##файл, где прописывается кто будет обрабатывать какой URL',
            'файл, описывающий относительные ссылки',
        ]
    },
    {
        'question': '[Django] Как указать url для главной страницы?',
        'type': Type.Single,
        'answers': [
            "##url(r'^$', HomeView.as_view())",
            "url(r'^home/$', HomeView.as_view())",
            "url(r'^index/$', HomeView.as_view())",
            "url(r'^index.html$', HomeView.as_view())",
        ]
    },
    {
        'question': '[Django] Что такое view?',
        'type': Type.Single,
        'answers': [
            "##Это обработчики запросов",
            "Это классы для отображения HTML",
            "Это шаблоны",
            "Это ссылки для шаблонов",
        ]
    },
    {
        'question': '[Django] Что такое templates?',
        'type': Type.Single,
        'answers': [
            "Это обработчики запросов",
            "Это классы для отображения HTML",
            "##Это шаблоны",
            "**Это html-файлы",
        ]
    },
    {
        'question': '[Django] Как запустить сайт локально?',
        'type': Type.Single,
        'answers': [
            "python manage.py localhost",
            "python manage.py localserver",
            "##python manage.py runserver",
            "localhost:8000",
        ]
    },
    {
        'question': '[Django] Что такое static файлы?',
        'type': Type.Single,
        'answers': [
            "Это js-файлы",
            "##Это неизменяемые файлы, которые Django не обрабатывает",
            "Это css-файлы",
            "Это файлы, которые генерирует Django по шаблону",
        ]
    },
    {
        'question': '[Django] Что нужно сделать чтобы файл был static?',
        'type': Type.Single,
        'answers': [
            "Файл должен быть либо js, либо css файлом",
            "##Файл должен находиться в static директории",
            "Нужно добавить в название файла static_",
            "В настройках Django указать",
        ]
    },
    {
        'question': '[Django] Что нужно сделать чтобы файл был static?',
        'type': Type.Single,
        'answers': [
            "Файл должен быть либо js, либо css файлом",
            "##Файл должен находиться в static директории",
            "Нужно добавить в название файла static_",
            "В настройках добавить этот файл в список static файлов",
        ]
    },
    {
        'question': '[Django] Что нужно, чтобы подключить static файл?',
        'type': Type.Multiple,
        'answers': [
            "##{% load staticfiles %}",
            "##{% static 'путь_до_static_файла' %}",
            "Добавить его в папку templates",
            "Написать <static></static> при подключении",
        ]
    },
    {
        'question': '[Django] Какие ключевые слова нужны чтобы расширить другой html-файл?',
        'type': Type.Multiple,
        'answers': [
            "##extends",
            "##block",
            "content",
            "body",
            "html",
        ]
    },
    {
        'question': '[Django] Какую СУБД использует Django по умолчанию?',
        'type': Type.Single,
        'answers': [
            "MySQL",
            "MS SQL",
            "##Sqlite",
            "Oracle",
        ]
    },
    {
        'question': '[Django] Что такое модели?',
        'type': Type.Single,
        'answers': [
            "😍Красивые девчонки и парни",
            "##Классы описывающие структуру БД",
            "Концептуальная модель приложения",
            "Описания структуры проекта",
        ]
    },
    {
        'question': '[Django] Какая команда создает и обновляет базу данных?',
        'type': Type.Single,
        'answers': [
            "makemigrations",
            "##migrate",
            "runserver",
            "create_db",
        ]
    },
    {
        'question': '[Django] Как создать таблицу в БД?',
        'type': Type.Single,
        'answers': [
            "##создать класс наследующий от класса models.Model",
            "выполнить команду python manage.py migrate",
            "CREATE TABLE название;",
            "Это мы не проходили 😝",
        ]
    },
    {
        'question': '[Django] Как получить список всех объектов модели Contact из БД?',
        'type': Type.Single,
        'answers': [
            "##Contact.objects.all()",
            "SELECT * from Contact;",
            "Contact.get_all()",
            "Contact.all()",
        ]
    },
    {
        'question': '[Django] Как получить список контактов начинаюшихся на "A"?',
        'type': Type.Single,
        'answers': [
            "##Contact.objects.filter(name_startswith='A')",
            "SELECT * from Contact WHERE name LIKE 'A%';",
            "Contact.get_contacts_startswith('A')",
            "Contact.filert(name_startswith='A')",
        ]
    },
]
