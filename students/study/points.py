# coding=utf-8
from students.model.base import Point


class Rating:
    def __init__(self, min, max, title, number):
        self.min = min
        self.max = max
        self.title = title
        self.number = number


Ratings = [
    Rating(0, 40, u"Рядовой", 1),
    Rating(40, 100, u"Младший сержант", 2),
    Rating(100, 160, u"Сержант", 3),
    Rating(160, 250, u"Старший сержант", 4),
    Rating(250, 320, u"Младший лейтенант", 5),
    Rating(320, 400, u"Лейтенант", 6),
    Rating(400, 500, u"Старший лейтенант", 7),
    Rating(500, 700, u"Капитан", 8),
    Rating(700, 1000, u"Майор", 9),
    Rating(1000, 1500, u"Подполковник", 10),
    Rating(1500, 2500, u"Полковник", 11),
    Rating(2500, 100000, u"Генерал-полковник", 12)
]


def get_rating(points):
    for rating in Ratings:
        if rating.min <= points < rating.max:
            return rating
    return Ratings[0]


class PointUtil:
    def __init__(self, student, course):
        self.student = student
        self.course = course

    def add_points(self, reason, points):
        point = Point(student=self.student, course=self.course, reason=reason, points=points)
        point.save()
