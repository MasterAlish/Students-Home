import random


class Type:
    Single = 'single'
    Multiple = 'multiple'
    Text = 'text'
    BigText = 'bigtext'


def arrange(question):
    ans = question['answers']
    for i in range(5):
        x = random.randint(0, len(ans) - 1)
        y = random.randint(0, len(ans) - 1)
        s = ans[x]
        ans[x] = ans[y]
        ans[y] = s
    question['answers'] = ans
    return question


def get_random_questions(questions, count):
    result = []
    selected = set([])
    while len(selected) < count:
        i = random.randint(0, len(questions) - 1)
        if i not in selected:
            selected.add(i)
            result.append(questions[i])
    return result
