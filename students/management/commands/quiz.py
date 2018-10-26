# coding=utf-8

from django.core.management import BaseCommand

from students.model.base import Quiz, QuizQuestion, QuizAnswer
from students.models import MyUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        single = "single"
        multiple = "multiple"
        text = "text"

        wrong = "wrong"
        right = "right"
        optional = "optional"
        css = Quiz.objects.create(name=u"Основы CSS")

        self.create_q(
            css, u"Укажите CSS свойство позволяющее устанавливать размер шрифта?", single,
            [
                (wrong, u"font-weight"),
                (right, u"font-size"),
                (wrong, u"weight"),
                (wrong, u"size"),
            ]
        )

        self.create_q(
            css, u"Укажите селектор позволяющий выбрать все элементы div имеющие атрибут id='wrap'", single,
            [
                (wrong, u"div-wrap"),
                (wrong, u"div id.wrap"),
                (wrong, u"div.wrap "),
                (right, u"div#wrap"),
            ]
        )

        self.create_q(
            css, u"С помощью какого тэга можно подключить к HTML документу внешний файл стилей?", single,
            [
                (wrong, u"<style>"),
                (right, u"<link>"),
                (wrong, u"<meta>"),
                (wrong, u"<css>"),
            ]
        )

        self.create_q(
            css, u"С помощью какого CSS свойства можно оформить границу элемента?", single,
            [
                (right, u"border"),
                (wrong, u"padding"),
                (wrong, u"margin"),
                (wrong, u"<outline>"),
            ]
        )

        self.create_q(
            css, u"Выберите свойство с правильно заданным значением цвета", single,
            [
                (right, u"color:#000000 "),
                (wrong, u"color:00-00-00"),
                (wrong, u"color:%00-00-00"),
                (wrong, u"color:#00:00:00"),
            ]
        )

        self.create_q(
            css, u"Выберите CSS свойство позволяющее скрыть элемент.", single,
            [
                (right, u"display"),
                (wrong, u"disappear"),
                (wrong, u"hide"),
                (wrong, u"show"),
            ]
        )

        self.create_q(
            css, u"Какие виды позиционирования элементов существуют в CSS?", multiple,
            [
                (right, u"relative"),
                (right, u"fixed"),
                (right, u"absolute"),
                (wrong, u"attached"),
            ]
        )

        self.create_q(
            css, u"Выберите псевдо-класс позволяющий оформить ссылки, на которые наведен курсор мыши.", single,
            [
                (right, u":hover "),
                (wrong, u":link"),
                (wrong, u":active"),
                (wrong, u":visited"),
            ]
        )

        self.create_q(
            css, u"Какое принципиальное отличие свойства ID от свойства CLASS", single,
            [
                (right, u"ID должен быть уникальным на странице, а одинаковый CLASS может быть у нескольких элементов "),
                (wrong, u"Разница только в наборе свойств, который может быть использован для этих селекторов. Например, для ID нельзя задавать свойство border, а для CLASS можно."),
                (wrong, u"CLASS должен быть уникальным на странице, а одинаковый ID может быть у нескольких элементов"),
                (wrong, u"Никакого отличия между ними нет."),
            ]
        )

        self.create_q(
            css, u"Какой CSS-код написан правильно?", single,
            [
                (right, u"div { border: 1px solid #ccc; }"),
                (wrong, u"<div> { border: 1px solid #ccc; }"),
                (wrong, u"div { border: 1px solid #hhh; }"),
                (wrong, u"<div> { border: 1px solid #hhh; }"),
            ]
        )

        self.create_q(
            css, u"Как изменить цвет фона для всех элементов h1 на странице?", single,
            [
                (right, u"h1 {background-color: #ccc;}"),
                (wrong, u"h1.all {background-color: #ccc;}"),
                (wrong, u"h1[all] {background-color: #ccc;}"),
                (wrong, u"h1:all {background-color: #ccc;}"),
            ]
        )

        self.create_q(
            css, u"Где можно указывать стили для веб-страницы?", multiple,
            [
                (right, u"во внешнем .css файле"),
                (right, u"внутри тега <style>"),
                (right, u"в атрибуте style любого html-элемента"),
                (wrong, u"в подключаемом .style файле"),
            ]
        )

        self.create_q(
            css, u"Если Петя напишет .object{color: red}, какие из нижеперечисленных элементов станут красными?", multiple,
            [
                (wrong, u"<div class='red'>Пианино</div>"),
                (right, u"<span class='object'>Арфа</span>"),
                (wrong, u"<object>Домино</object>"),
                (optional, u"<div style='color:red;'>Петарды</div>"),
            ]
        )

        self.create_q(
            css, u"Что означает селектор 'table.big td'?", single,
            [
                (right, u"Все <td> внутри таблицы с классом big"),
                (wrong, u"Все <td> с классом big внутри таблицы"),
                (wrong, u"Все <table> с классом big внутри <td>"),
                (wrong, u"Запарило меня это все"),
            ]
        )

        js = Quiz.objects.create(name=u"Основы JS и jQuery")

        self.create_q(
            js, u"В каком теге подколючается JS файл?", single,
            [
                (right, u"<script>"),
                (wrong, u"<js>"),
                (wrong, u"<javascript>"),
                (wrong, u"<head>"),
            ]
        )

        self.create_q(
            js, u"Как объявить переменную code в JS?", single,
            [
                (wrong, u"def code;"),
                (right, u"var code;"),
                (wrong, u"String code;"),
                (wrong, u"code = var;"),
            ]
        )

        self.create_q(
            js, u"Как показать окно с сообщением в JS?", single,
            [
                (wrong, u"dialog();"),
                (right, u"alert();"),
                (wrong, u"show();"),
                (wrong, u"message();"),
            ]
        )

        self.create_q(
            js, u"Как указать тип переменной в JS?", single,
            [
                (right, u"Типы не указываются"),
                (wrong, u"Перед названием переменной"),
                (wrong, u"После название переменной"),
                (wrong, u"В функции"),
            ]
        )

        self.create_q(
            js, u"Как создать массив элементов в JS?", single,
            [
                (right, u"var d = [1,2,3,4];"),
                (wrong, u"var d[1,2,3,4];"),
                (wrong, u"array d = [1,2,3,4];"),
                (wrong, u"var d = {1,2,3,4};"),
            ]
        )

        self.create_q(
            js, u"JS: Что вернет typeof(5)?", single,
            [
                (right, u"'number'"),
                (wrong, u"'int'"),
                (wrong, u"'integer'"),
                (wrong, u"'float'"),
            ]
        )

        self.create_q(
            js, u"JS: Какие типы данных существуют?", multiple,
            [
                (right, u"number"),
                (right, u"null"),
                (right, u"undefined"),
                (right, u"boolean"),
            ]
        )

        self.create_q(
            js, u"Что такое объект в JS?", single,
            [
                (right, u"Стуктура данных где хранятся разные значения по ключам"),
                (wrong, u"Элемент в котором хранятся данные"),
                (wrong, u"Реализация класса"),
                (wrong, u"Обычно это браузер"),
            ]
        )

        self.create_q(
            js, u"Что нужно сделать в jQuery чтобы получить все <div>?", single,
            [
                (right, u"$('div')"),
                (wrong, u"$.find('div')"),
                (wrong, u"all('div')"),
                (wrong, u"$('.div')"),
            ]
        )

        self.create_q(
            js, u"Как в jQuery получить текст текущего элемента?", single,
            [
                (right, u"$(this).text()"),
                (wrong, u"$(this).text"),
                (wrong, u"$(this).gettext()"),
                (wrong, u"$(this).item()"),
            ]
        )

        self.create_q(
            js, u"Как в у всех <h2> поменять цвет текста на красный в jQuery?", single,
            [
                (right, u"$('h1').css('color', 'red');"),
                (wrong, u"$('h1').color('red');"),
                (wrong, u"$('h1:color').css('red');"),
                (wrong, u"h1.css('color', 'red');"),
            ]
        )

        self.create_q(
            js, u"Как вызвать функуию onLoad после загрузки страницы в jQuery?", single,
            [
                (right, u"$(document).ready(onLoad);"),
                (wrong, u"$(document).onReady(onLoad);"),
                (wrong, u"$(document).on('ready', onLoad);"),
                (wrong, u"onLoad()"),
            ]
        )

        self.create_q(
            js, u"Как при клике на элемент с классом block делать его невидимым?", multiple,
            [
                (right, u"$('.block').on('click', function(){$(this).css('display', 'none');});"),
                (wrong, u"$('#block').on('click', function(){$(this).css('display', 'none');});"),
                (wrong, u"$('.block').on('click', function(){$(this).css('block', 'none');});"),
                (right, u"$('.block').on('click', function(){$(this).hide();});"),
            ]
        )

        cg = Quiz.objects.create(name=u"Основы Комп Графики")

        self.create_q(
            cg, u"Свет это - ", single,
            [
                (right, u"Электромагнитное излучение"),
                (wrong, u"Психологическое восприятие яркости"),
                (wrong, u"Химическое свойство молекул"),
                (wrong, u"Начало всех начал"),
            ]
        )

        self.create_q(
            cg, u"Какие существуют спектры электромагнитных излучений?", multiple,
            [
                (right, u"Видимый свет"),
                (right, u"Гамма излучения"),
                (right, u"Рентгеновские лучи"),
                (right, u"Радио волны"),
                (right, u"Ультрафиолетовые лучи"),
            ]
        )

        self.create_q(
            cg, u"Какие называется спектр электромагнитных излучений, который виден человеку?", single,
            [
                (right, u"Видимый свет"),
                (wrong, u"Спектр глаза человека"),
                (wrong, u"Инфракрасный спектр"),
                (wrong, u"Радужный спектр"),
            ]
        )

        self.create_q(
            cg, u"Какие рецепторы света есть в сетчатке глаза?", multiple,
            [
                (right, u"Колбочки"),
                (right, u"Палочки"),
                (wrong, u"Трубочки"),
                (wrong, u"Кружочки"),
            ]
        )

        self.create_q(
            cg, u"Какой цвет получится если смешать красный и зеленый цвета?", single,
            [
                (right, u"Желтый"),
                (wrong, u"Красный"),
                (wrong, u"Синий"),
                (wrong, u"Фиолетовый"),
            ]
        )

        self.create_q(
            cg, u"Что такое цветовое пространство?", single,
            [
                (right, u"Система координат, которая позволяет однозначно определить цвет"),
                (wrong, u"Пространство в котором расположены весь спектр излучений"),
                (wrong, u"Это RGB"),
                (wrong, u"Это изулучение в диапозоне от 400 до 700 нм"),
            ]
        )

        self.create_q(
            cg, u"Какие существуют цветовые пространства?", multiple,
            [
                (right, u"RGB"),
                (right, u"CMY"),
                (right, u"CIE LAB"),
                (right, u"XYZ"),
            ]
        )

        self.create_q(
            cg, u"Что такое RGB?", single,
            [
                (right, u"Это цветовое пространство, где любой цвет можно представить смешением трех основных цветов Red, Green и Blue"),
                (wrong, u"Это технология которая используется для передачи цвета в телефизорах"),
                (wrong, u"Это автоматизированная программа разработанная DARPA для разделения цветов"),
            ]
        )

        self.create_q(
            cg, u"Что из этого правда про CMY?", multiple,
            [
                (right, u"Цветовое пространство где основными цветами является Голубой, Пурпурный и Желтый"),
                (right, u"Антипод RGB. Желтая краска не отражает синий, голубая красный, пурпуная не отражает зеленый"),
                (right, u"Используется в цветных принтерах"),
                (right, u"Есть расширенная модель CMYK, где K-это в основном черный цвет"),
            ]
        )

        self.create_q(
            cg, u"Чем цветовое пространство HSI лучше RGB и CMY?", single,
            [
                (right, u"Основан на человеческом восприятии цвета"),
                (wrong, u"Лучше обрабатывается программно"),
                (wrong, u"При кодировании цвета получаем меньший размер цвета"),
                (wrong, u"Пространства намного больше"),
            ]
        )

        self.create_q(
            cg, u"Что такое растровая графика?", single,
            [
                (right, u"Изображение состоит из пикселей, каждый из которых имеет свой цвет"),
                (wrong, u"Изображение состоит из геометрических фигур"),
                (wrong, u"Изображение использует только цвета RGB"),
                (wrong, u"Изображение где нет прозрачных частей"),
            ]
        )

        self.create_q(
            cg, u"Откуда начинается ос OY на компьютере?", single,
            [
                (right, u"С верхней точки экрана и увеличивается вниз"),
                (wrong, u"С нижней точки экрана и увеличивается вверх"),
                (wrong, u"С верхней левой точки экрана и увеличивается по диагонали"),
                (wrong, u"С нижней левой точки экрана и увеличивается вверх по диагонали"),
            ]
        )

        self.create_q(
            cg, u"Как нарисовать горизонтальную линию в середине экрана?", single,
            [
                (right, u"drawLine(0, height/2, width, height/2)"),
                (wrong, u"drawLine(0, height, width, height/2)"),
                (wrong, u"drawLine(width/2, height/2, width/2, height/2)"),
                (wrong, u"drawLine(width/2, 0, width/2, height)"),
            ]
        )

        self.create_q(
            cg, u"Как нарисовать вертикальную линию в середине экрана?", single,
            [
                (right, u"drawLine(width/2, 0, width/2, height)"),
                (wrong, u"drawLine(0, height, width, height/2)"),
                (wrong, u"drawLine(width/2, height/2, width/2, height/2)"),
                (wrong, u"drawLine(0, height/2, width, height/2)"),
            ]
        )

        self.create_q(
            cg, u"Что такое матричный фильтр?", single,
            [
                (right, u"Способ обработки изображений умножением матрицы коеффициентов на матрицу пикселей"),
                (wrong, u"Фильтр позволяющий получать более высокую насыщенность цветов при обработке"),
                (wrong, u"Экран в цифровых камерах, который не впускает нежелательный свет"),
                (wrong, u"Способ фильтрации цвета при обработке гамма излучений"),
            ]
        )

        self.create_q(
            cg, u"Какого размера должны быть матричные фильтры?", single,
            [
                (right, u"Главное больше чем 1х1, чем больше тем качественнее обработка"),
                (wrong, u"Только 3х3 и 4х4"),
                (wrong, u"Главное чтобы матрица была квадратной"),
                (wrong, u"5х5"),
            ]
        )

        self.create_q(
            cg, u"Какой класс используются для обработки изображений в Java?", single,
            [
                (right, u"BufferedImage"),
                (wrong, u"Image"),
                (wrong, u"ImageInMemory"),
                (wrong, u"JFrame"),
            ]
        )

        unity = Quiz.objects.create(name=u"Основы Unity3D")

        self.create_q(
            unity, u"Что такое Unity3D?", single,
            [
                (right, u"Движок и среда для создания игр и приложений"),
                (wrong, u"Библиотека для обработки 3D изображений"),
                (wrong, u"Программа для просмотра 3D объектов"),
                (wrong, u"Игра"),
            ]
        )

        self.create_q(
            unity, u"Зачем нужен Collider в Unity?", single,
            [
                (right, u"Для определения границ столкновения"),
                (wrong, u"Для запуска частиц на большой скорости"),
                (wrong, u"Он там вообще не нужен"),
                (wrong, u"А что это такое?"),
            ]
        )

        self.create_q(
            unity, u"Чем отличается 2D от 3D?", single,
            [
                (right, u"В 3D есть объем и глубина"),
                (wrong, u"В 3D качество обычно намного лучше"),
                (wrong, u"В 3D игры намного интереснее"),
                (wrong, u"Разницы особой нет. А вот 5D и 7D это нечто!"),
            ]
        )

        self.create_q(
            unity, u"Что такое Rigidbody?", single,
            [
                (right, u"Компонент дающий игровому объекту твердость и вес"),
                (wrong, u"Компонент определяющий столкновения объектов"),
                (wrong, u"Компонент отображающий изображение"),
                (wrong, u"Компонент позволяюший управлять объектом"),
            ]
        )


    def create_q(self, quiz, text, _type, answers):
        q = QuizQuestion.objects.create(text=text, type=_type, quiz=quiz)
        for answer_type, answer in answers:
            QuizAnswer.objects.create(question=q, text=answer, type=answer_type)
