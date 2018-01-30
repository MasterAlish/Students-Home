# coding=utf-8
from students.management.commands.tests import Type


questions = [
    {
        'question': 'Кто(где, что) выполняет программу написанную на языке Java?',
        'type': Type.Single,
        'answers': [
            '##JVM(Виртуальная машина Java)',
            'OC(операционная система)',
            'Компьютер, кто же еще',
            'Java runner(выполнитель Java программ)'
        ]
    },
    {
        'question': 'Из чего состоит программа на Java?',
        'type': Type.Single,
        'answers': [
            '##Из классов',
            'Из комманд',
            'Из подпрограмм',
            'Из переменных'
        ]
    },
    {
        'question': 'Как должен называться файл в котором находится класс Java?',
        'type': Type.Single,
        'answers': [
            'Так же как класс',
            '##Так же как класс с расширением .java',
            'Главное чтобы пробелов в названии не было',
            'public class'
        ]
    },
    {
        'question': 'Как можно вывести текст в консоль?',
        'type': Type.Single,
        'answers': [
            '##System.out.print("Этот ответ наверное неправильный")',
            'System.in.println("Выбери меня!")',
            'System.console.println("В консоль же нужно вывести")',
            'print "Все гениальное просто!"'
        ]
    },
    {
        'question': 'Какой метод запускается при выполнении класса?',
        'type': Type.Single,
        'answers': [
            '##public static void main(String[] params)',
            'public static void Main(String[] params)',
            'public static void Main(String[] args)',
            'public static void main(String args)'
        ]
    },
    {
        'question': 'Какие "примитивные" типы существуют в Java?',
        'type': Type.Multiple,
        'answers': [
            '##int',
            'void',
            'null',
            '##char',
            '##boolean',
            'String',
            'Double'
        ]
    },
    {
        'question': 'Какой метод ничего не возвращает?',
        'type': Type.Single,
        'answers': [
            '##public void string()',
            'public static String curl()',
            'public Null nullable() ',
            'private int emptyMethod()',
        ]
    },
    {
        'question': 'Какой тип лучше использовать для математических вычислений по физике?',
        'type': Type.Single,
        'answers': [
            'int',
            '##double',
            'float',
            'long',
        ]
    },
    {
        'question': 'Что такое объект?',
        'type': Type.Single,
        'answers': [
            '**Все что можно потрогать, увидеть, описать и т.д.',
            'Противоположное от субъекта',
            '##Это что-то созданное по определенному классу',
            'Яблоко - это объект',
        ]
    },
    {
        'question': '<div class="code">Tree tree = new Tree();</div> Tree - дерево с английского. Что тут написано?',
        'type': Type.Single,
        'answers': [
            '##Создается новое дерево',
            'Написано что дерево это новое дерево',
            'Описывается класс Tree',
        ]
    },
    {
        'question': 'Какие из нижеперечисленных утверждений правильны?',
        'type': Type.Multiple,
        'answers': [
            '**Я стану крутым программистом!',
            '**Мне нравится программировать',
            '**Сегодня погода хорошая',
            '**Я получу хороший бал за этот тест',
        ]
    },
    {
        'question': 'Какие из нижеперечисленных утверждений правильны?',
        'type': Type.Multiple,
        'answers': [
            '##Класс - это описание какой-то сущности',
            '##По описанному классу создаются конкретные объекты',
            '##Объекты находятся в памяти',
            '##Java - объектноориентированный язык',
        ]
    },
    {
        'question': 'Сколько значений можно хранить в одной переменной?',
        'type': Type.Single,
        'answers': [
            'Сколько угодно',
            '##Одно',
            'Два',
            'Зависит уровня сложности переменной',
        ]
    },
    {
        'question': '<div class="code">int balance = 100;<br>balance = balance-balance;</div>  Какое значение будет в переменной balance?',
        'type': Type.Single,
        'answers': [
            '##0',
            '-100',
            '-1',
            'никакое',
        ]
    },
    {
        'question': '<div class="code">double size = 3.14; </div>Выберите правильные утверждения',
        'type': Type.Multiple,
        'answers': [
            '##size - это переменная',
            '##double - это тип переменной',
            '##3.14 - это присваиваемое значение',
            'Нельзя хранить в переменной типа double значение 3.14',
        ]
    },
    {
        'question': 'Про пакеты можно сказать следующее',
        'type': Type.Multiple,
        'answers': [
            '##Пакеты помогают упорядочить классы',
            '##В одном пакете могут быть несколько классов',
            '##Пакеты это папки',
            '**Пакеты должны быть экологическими',
        ]
    },
    {
        'question': '<div class="code">boolean sunny = True;<br>int temp = 20;<br>if(sunny && temp>15){<br>'
                    '<span class="tab"></span>System.out.println("Я хочу на улицу");<br>} else {<br>'
                    '<span class="tab"></span>System.out.println("Я лучше посплю");<br>}</div>Что напечает этот участок кода?',
        'type': Type.Single,
        'answers': [
            'Ничего',
            '##Я лучше посплю',
            'Я хочу на улицу',
            'Ошибка в коде',
        ]
    },
    {
        'question': 'Класс состоит из свойств и методов, да?',
        'type': Type.Single,
        'answers': [
            '##Да',
            'Нет',
            'Скорее да, чем нет',
        ]
    },
    {
        'question': 'Где указывается возвращаемый тип метода?',
        'type': Type.Single,
        'answers': [
            'В конце',
            'В начале',
            '##Перед названием',
            'Внутри скобок',
        ]
    },
    {
        'question': 'Где неправильно вызывается метод?',
        'type': Type.Single,
        'answers': [
            'this.charge();',
            'charge(34);',
            'int d = getSum();',
            '##setSize(int 4);',
        ]
    },
    {
        'question': 'Какой метод вызывается при создании объекта?',
        'type': Type.Single,
        'answers': [
            'Метод main()',
            '##Конструктор',
            'Первый метод',
            'Метод который указан',
        ]
    },
    {
        'question': 'Объявление массива',
        'type': Type.Single,
        'answers': [
            '##int[] gopro',
            'Array array',
            'new String[]',
            'int[4]',
        ]
    },
    {
        'question': 'Как взять первый элемент массива?',
        'type': Type.Single,
        'answers': [
            '##items[0]',
            'items[1]',
            'items.getFirst()',
            'items.1',
        ]
    },
    {
        'question': 'Как получить длину массива?',
        'type': Type.Single,
        'answers': [
            '##array.length',
            'array.length()',
            'array.getLen()',
            'array.size',
        ]
    },
    {
        'question': 'Можно менять длину массива int[]?',
        'type': Type.Single,
        'answers': [
            'Да',
            '##Нет',
            'Скорее нет, чем да',
        ]
    },
    {
        'question': 'Какой цикл неправильный?',
        'type': Type.Single,
        'answers': [
            'for(String name: names){...}',
            'for(int i=0;i<10;i++){...}',
            'while(True){...}',
            '##while(int i=0;i++){...}',
        ]
    },
    {
        'question': 'Какой цикл бесконечный?',
        'type': Type.Multiple,
        'answers': [
            '##for(;;){...}',
            '##for(int i=0;i<10;i--){...}',
            '##while(True){...}',
            'while(False){...}',
        ]
    },
    {
        'question': 'Какое ключевое слово позволяет выйти из цикла?',
        'type': Type.Single,
        'answers': [
            '##break',
            'continue',
            'new',
            'label',
        ]
    },
    {
        'question': 'Сколько раз выполнится этот цикл<div class="code">'
                    'int i=6;<br>'
                    'while(i>0){<br>'
                    '<span class="space"></span>i = i-2;<br>'
                    '<span class="space"></span>System.out.println(i);<br>'
                    '}'
                    '</div> ?',
        'type': Type.Single,
        'answers': [
            '##3',
            '6',
            '2',
            '0',
        ]
    },
    {
        'question': 'Что нужно сделать перед использоваем других классов?',
        'type': Type.Single,
        'answers': [
            '##Подключить их с помощью оператора import',
            'Создать их с помощью new',
            'Объявить их как package',
            'public static void main()',
        ]
    },
    {
        'question': 'Как мы можем расширить имеющийся класс?',
        'type': Type.Single,
        'answers': [
            '##С помощью наследования',
            'С помощью интерфейсов',
            'С помощью асбстракций',
            'Написать private',
        ]
    },
    {
        'question': 'Какой модификатор доступа неправильный?',
        'type': Type.Single,
        'answers': [
            'public',
            'private',
            '##static',
            'protected',
        ]
    },
    {
        'question': 'Сколько методов может переопределить дочерний класс?',
        'type': Type.Single,
        'answers': [
            '##Сколько угодно',
            'На один меньше чем у родителя',
            'Один',
        ]
    },
    {
        'question': '<div class="code">public class Car extends Transport</div> Какое из утверждений правильно?',
        'type': Type.Single,
        'answers': [
            '##класс Transport родитель класса Car',
            'класс Car родитель класса Transport',
            'класс Car заменяет класс Transport',
            'класс Transport расширяет класс Car',
        ]
    },
    {
        'question': 'Если переопределить метод класса, то?',
        'type': Type.Single,
        'answers': [
            'при вызове этого метода у объекта дочернего класса, ничего не произойдет',
            'метод станет доступным извне',
            '##метод дочернего класса заменит метод класса-родителя в дочернем классе',
        ]
    },
    {
        'question': 'Метод можно вызвать у..',
        'type': Type.Multiple,
        'answers': [
            '##классов',
            '##объектов',
            'примитивных типов',
            'пакетов',
        ]
    },
    {
        'question': 'Родитель всех классов это - ',
        'type': Type.Single,
        'answers': [
            '##класс Object',
            'Адам',
            'класс Parent',
        ]
    },
    {
        'question': 'Какой код ошибочный?',
        'type': Type.Single,
        'answers': [
            'int i = Integer.parseInt("3");',
            'String s = "master";',
            'Object o = new Document();',
            '##int o = new int();',
        ]
    },
    {
        'question': 'Какой код ошибочный?',
        'type': Type.Single,
        'answers': [
            'String i = Integer.parseInt("3");',
            '##int s = "34";',
            'double d = 3.34433;',
            "char c = '4';",
        ]
    },
    {
        'question': 'Какой код ошибочный?',
        'type': Type.Single,
        'answers': [
            'for(i=0;i<9;i++)',
            'for(int i=0;i<10;i=i+2)',
            '##for(int i=0;i++;)',
            "for(;;)",
        ]
    },
    {
        'question': 'Какой код ошибочный?',
        'type': Type.Single,
        'answers': [
            '##string str = "alma";',
            'int alma = 34;',
            "char symbol_x = 'x';",
            "boolean yes = True;",
        ]
    },
    {
        'question': 'Если Яблоко наследует Фрукт. А Маша ест только фрукты. Можем ли Маша съесть яблоко?',
        'type': Type.Single,
        'answers': [
            '##Да, потому что яблоко тоже фрукт',
            'Нет, потому что в программамирование нет понятий яблоко и фрукты',
            "Нет, потому что яблоко может отличаться от фрукта",
            "Да, интуиция подсказывает",
        ]
    },
    {
        'question': 'Если у класса Фигура есть дочерние классы: Квадрат, Трапеция. То ..',
        'type': Type.Single,
        'answers': [
            'Квадрат может заменять Фигуру, потому что Квадрат это полноценная Фигура',
            'Фигура может заменять Трапецию, потому что Трапеция это полноценная Фигура',
            "Такое невозможно, в Java нет множественного наследования",
        ]
    },
    {
        'question': 'Что такое интерфейс в Java?',
        'type': Type.Single,
        'answers': [
            'Описание структуры класса',
            '##Список методов, которые нужно реализовать',
            "Способ взаимодействия с внешними классами",
        ]
    },
    {
        'question': 'Можно ли создавать объект класса?',
        'type': Type.Single,
        'answers': [
            '##Да',
            'Нет',
        ]
    },
    {
        'question': 'Можно ли создавать объект интерфейса?',
        'type': Type.Single,
        'answers': [
            'Да',
            '##Нет',
        ]
    },
    {
        'question': 'Коллекции это - ?',
        'type': Type.Single,
        'answers': [
            'Хранилища классов',
            '##Хранилища объектов',
            'Это массивы данных',
            'Это разные типа переменных',
        ]
    },
    {
        'question': 'List, Map, Set это -  ?',
        'type': Type.Single,
        'answers': [
            'классы',
            '##интрефейсы',
            'пакеты',
            'объекты',
        ]
    },
    {
        'question': '<div class="code">List list = new List(); </div>это  правильно ?',
        'type': Type.Single,
        'answers': [
            'Да, создается новый список',
            'Нет, массивы создаются с помощью []',
            '##Нет, List это не класс, а интерфейс',
            'Да',
        ]
    },
    {
        'question': '<div class="code">List list = new ArrayList(); </div>это  правильно ?',
        'type': Type.Single,
        'answers': [
            '##Да, создается новый список',
            'Нет, массивы создаются с помощью []',
            'Нет, List это не класс, а интерфейс',
            'Нет',
        ]
    },
    {
        'question': 'Map это - ?',
        'type': Type.Single,
        'answers': [
            '##Ассоциативный массив где значения хранятся по ключу',
            'Это класс который хранит карту мира',
            'Это класс который описывает список',
        ]
    },
    {
        'question': 'HashSet - это реализация интерфейса Set, который описывает неповторяемое множество объектов',
        'type': Type.Single,
        'answers': [
            '##Правильно',
            'Неправильно',
            'Это словарь',
        ]
    },
    {
        'question': 'Как узнать длину обычных коллекций?',
        'type': Type.Single,
        'answers': [
            '##size()',
            'length()',
            'length',
            'getCount()',
        ]
    },
    {
        'question': 'Как добавить элемент в список List?',
        'type': Type.Single,
        'answers': [
            '##list.add(element)',
            'list = new Element()',
            'list[0] = element;',
        ]
    },
    {
        'question': 'У Generic классов тип указывается так:',
        'type': Type.Single,
        'answers': [
            '##List<String>',
            'String[]',
            '(String string)',
        ]
    },
    {
        'question': 'Как обработать ошибку?',
        'type': Type.Single,
        'answers': [
            '##поймать ключевыми словами try, catch',
            'поймать ключевым словом break',
            'Наследовать от класса Exception',
            'ключевым словом finally',
        ]
    },
    {
        'question': 'Во что компилируется программа написанная на языке Java?',
        'type': Type.Single,
        'answers': [
            '##Байт-код',
            'Бит-код',
            'Машинные команды',
            'Assembler',
        ]
    },
    {
        'question': '<div class="code">"Алма-Ата".substring(5);</div> что вернет данный код?',
        'type': Type.Single,
        'answers': [
            '##"Ата"',
            '"Алма"',
            'Произойдет ошибка',
            'Код даже не скомпилируется',
        ]
    }
]