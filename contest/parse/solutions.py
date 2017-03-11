import re
from lxml import html, etree

from contest.models import ProblemSolution


class SolutionParser(object):
    def __init__(self, text):
        self.text = text

    def parse(self):
        solution = {}
        tree = html.fromstring(self.text)
        for elem in tree.xpath("//table[contains(@class, 'status')]//tr"):
            row_html = etree.tostring(elem, pretty_print=True)
            if not 'class="header"' in row_html:
                solution['acm_id'] = int(re.compile('class="id">(\d+)</td>').findall(row_html)[0])
                solution['username'] = re.compile('aspx\?id=\d+">(.+)</a>').findall(row_html)[0]
                solution['language'] = re.compile('class="language">(.+)</td>').findall(row_html)[0]
                try:
                    solution['check_result'] = re.compile('class="verdict.*">(.+)</td>').findall(row_html)[0]
                except:
                    solution['check_result'] = re.compile('rel="nofollow">(.*)</a>').findall(row_html)[0]
                try:  solution['test_number'] = int(re.compile('class="test">(\d+)</td>').findall(row_html)[0])
                except: solution['test_number'] = None
                try:  solution['time'] = re.compile('class="runtime">(.*)</td>').findall(row_html)[0]
                except: solution['time'] = None
                try:  solution['memory'] = re.compile('class="memory">(.*)</td>').findall(row_html)[0]
                except: solution['memory'] = None
                solution['success'] = solution['check_result'] == 'Accepted'
                break
        return solution

    def parse_and_fill(self, solution):
        solution_data = self.parse()
        solution.acm_id = solution_data['acm_id']
        solution.language = solution_data['language']
        solution.check_result = solution_data['check_result']
        solution.time = solution_data['time']
        solution.memory = solution_data['memory']
        solution.test_number = solution_data['test_number']
        solution.success = solution_data['success']
        return solution
