# coding=utf-8

from students.management.commands.tests import Type

questions = [
    {
        'question': 'Какие из нижеперечисленных Виртуальных машин используется в Андроид?',
        'type': Type.Multiple,
        'answers': [
            '##ART',
            '##Dalvik',
            'JVM',
            'JIT',
        ]
    },
    {
        'question': 'Какое ядро использует ОС Андроид?',
        'type': Type.Single,
        'answers': [
            '##Linux',
            'Unix',
            'Windows NT',
            'OS/2',
        ]
    },
    {
        'question': 'Что из перечисленного входит в Андроид приложение?',
        'type': Type.Multiple,
        'answers': [
            '##Файл AndroidManifest.xml',
            '##Ресурсы',
            '##Классы Java',
        ]
    },
    {
        'question': 'Сколько потоков можно создавать в приложении Андроид?',
        'type': Type.Single,
        'answers': [
            'Только UI Thread',
            'Зависит от уровня API',
            'Основной поток и фоновый поток',
            '##Неограниченное количество',
        ]
    },
    {
        'question': 'Как называется основной класс Андроид, который позволяет создавать "окна"?',
        'type': Type.Single,
        'answers': [
            '##Activity',
            'Service',
            'Intent',
            'Window',
        ]
    },
    {
        'question': 'Базовый класс всех элементов пользовательского интерфейса Андроид?',
        'type': Type.Single,
        'answers': [
            '##View',
            'Interface',
            'Form',
            'Window',
        ]
    },
    {
        'question': 'Какой класс позволяет взаимодействовать разным Activity?',
        'type': Type.Single,
        'answers': [
            'Messanger',
            'Service',
            '##Intent',
            'Window',
        ]
    },
    {
        'question': 'Что обязательно нужно сделать, чтобы создать форму в Андроид?',
        'type': Type.Multiple,
        'answers': [
            '##Наследовать от класса Activity',
            '##Объявить наше Activity в AndroidManifest',
            'Создать объект класса Intent',
            '**Связать Activity с одним layout-файлом',
        ]
    },
    {
        'question': 'В какой папке ресурсов хранятся картинки в Андроид?',
        'type': Type.Single,
        'answers': [
            '##drawable',
            'images',
            'img',
            'pictures',
        ]
    },
    {
        'question': 'В какой папке ресурсов хранятся описания пользовательского интерфейса в Андроид?',
        'type': Type.Single,
        'answers': [
            'drawable',
            '##layouts',
            'mipmap',
            'assets',
        ]
    },
    {
        'question': 'Какие состояния есть у Activity?',
        'type': Type.Multiple,
        'answers': [
            '##Остановлен(Stopped)',
            '##Приостановлен(Paused)',
            '##Активен(Resumed)',
            'Закрыто(Closed)',
        ]
    },
    {
        'question': 'Какие параметры обязательные для View элементов?',
        'type': Type.Multiple,
        'answers': [
            '##layout_width',
            '##layout_height',
            'layout_gravity',
            'background',
        ]
    },
    {
        'question': 'Какой параметр отвечает за выравнивание?',
        'type': Type.Single,
        'answers': [
            'orientation',
            'text_align',
            '##gravity',
            'align',
        ]
    },
    {
        'question': 'Какой view-элемент используется для вывода текста?',
        'type': Type.Single,
        'answers': [
            '##TextView',
            'EditText',
            'ListView',
            'LinearLayout',
        ]
    },
    {
        'question': 'Какой view-элемент используется для вывода изображения?',
        'type': Type.Single,
        'answers': [
            'TextView',
            '##ImageView',
            'ListView',
            'LinearLayout',
        ]
    },
    {
        'question': 'Какой view-group-элемент группирует элементы по вертикали или по горизонтали?',
        'type': Type.Single,
        'answers': [
            'RelativeLayout',
            'GridLayout',
            'FrameLayout',
            '##LinearLayout',
        ]
    },
    {
        'question': 'Что означает ключевое слово wrap_content?',
        'type': Type.Single,
        'answers': [
            'Соответствует длине родителя',
            '##Соответствует длине содержимого',
            'Занимать половину экрана',
        ]
    },
    {
        'question': 'Какой это цвет #FF0000 ?',
        'type': Type.Single,
        'answers': [
            '##Красный',
            'Синий',
            'Зеленый',
        ]
    },
    {
        'question': 'Как нужно ссылаться на картинку из layout-файла?',
        'type': Type.Single,
        'answers': [
            '##@drawable/image_name',
            'image_name',
            'getImageByID("image_name")',
        ]
    },
    {
        'question': 'С помощью какого метода устанливается обработчик клика?',
        'type': Type.Single,
        'answers': [
            '##setOnClickListener()',
            'onClick()',
            'dispatchClickEvent()',
        ]
    },
    {
        'question': 'Какой класс позволяет писать в лог Андроид?',
        'type': Type.Single,
        'answers': [
            'Logger',
            '##Log',
            'System.out',
        ]
    },
    {
        'question': 'Как называются аргументы передаваемые с помощью класса Intent?',
        'type': Type.Single,
        'answers': [
            '##Extras',
            'Arguments',
            'Parameters',
            'Values',
        ]
    },
    {
        'question': 'Сколько всего разных разрешений в Android?',
        'type': Type.Single,
        'answers': [
            '**4',
            '**8',
            '**16',
            '**32',
        ]
    },
    {
        'question': 'SharedPreferences это?',
        'type': Type.Single,
        'answers': [
            'Круто!',
            '##Класс позволяющий сохранять разные настройки приложения',
            'Система управления базами данных',
            'Нет правильного ответа',
        ]
    },
    {
        'question': 'Какой СУБД используется в Андроид?',
        'type': Type.Single,
        'answers': [
            'MySQL',
            'Oracle',
            '##SQlite',
            'PostgreSQL',
        ]
    }
]
