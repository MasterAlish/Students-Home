import re
import requests
from lxml import html
from lxml.html import tostring

from contest.models import Problem


class ProblemParser(object):
    def __init__(self, url):
        if '&locale=ru' in url:
            self.url = url
        else:
            self.url = url + '&locale=ru'

    def parse(self):
        problem = Problem(url=self.url)
        response = requests.get(self.url)
        if response.status_code == 200:
            tree = html.fromstring(response.text)
            problem.title = self.parse_title(tree)
            problem.acm_id = self.parse_id(problem.title)
            problem.difficulty = self.parse_difficulty(tree)
            problem.limits = self.parse_limits(tree)
            problem.body = self.parse_body(tree)
        return problem

    def parse_body(self, tree):
        body_parts = tree.xpath("//div[@id='problem_text']/node()")
        body = u""
        for part in body_parts:
            body += tostring(part)
        return body

    def parse_limits(self, tree):
        parts = tree.xpath("//div[@class='problem_limits']/text()")
        limits = u""
        for part in parts:
            limits += part+u"<br>"
        return limits

    def parse_title(self, tree):
        return tree.xpath("//h2[@class='problem_title']/text()")[0]

    def parse_difficulty(self, tree):
        try:
            text = tree.xpath("//div[@class='problem_links']/span/text()")[0]
            pattern = re.compile("(\d+)$")
            return int(pattern.findall(text)[0])
        except:
            return 0

    def parse_id(self, title):
        pattern = re.compile("^(\d+)\.")
        return int(pattern.findall(title)[0])

