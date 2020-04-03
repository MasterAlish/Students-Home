# coding=utf-8
from students.model.base import Point


class Rating:
    def __init__(self, min, max, title, number):
        self.min = min
        self.max = max
        self.title = title
        self.number = number


Ratings = [
    Rating(0, 20, u"10 кю", 1),
    Rating(20, 50, u"9 кю", 2),
    Rating(50, 80, u"8 кю", 3),
    Rating(80, 120, u"7 кю", 4),
    Rating(120, 160, u"6 кю", 5),
    Rating(160, 200, u"5 кю", 6),
    Rating(200, 250, u"4 кю", 7),
    Rating(250, 300, u"3 кю", 8),
    Rating(300, 350, u"2 кю", 9),
    Rating(350, 400, u"1 кю", 10),
    Rating(400, 500, u"1 дан", 11),
    Rating(500, 600, u"2 дан", 12),
    Rating(600, 700, u"3 дан", 13),
    Rating(700, 800, u"4 дан", 14),
    Rating(800, 900, u"5 дан", 15),
    Rating(900, 1000, u"6 дан", 16),
    Rating(1000, 1100, u"7 дан", 17),
    Rating(1100, 1200, u"8 дан", 18),
    Rating(1200, 1500, u"9 дан", 19),
    Rating(1500, 100000, u"10 дан", 20)
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
