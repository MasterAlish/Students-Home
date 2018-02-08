import random

from slugify import slugify


def random_letter():
    letters = "1234567890qwertyuiopasdfghjklzxcvbnm"
    return letters[random.randint(0, len(letters)-1)]


def my_unique_slugify(model, text):
    for i in range(1000):
        random_letter()
    slug = slugify(text)
    if len(slug) > 255:
        slug = slug[:200]
    while model.objects.filter(slug=slug).exists():
        slug += random_letter()
    return slug
