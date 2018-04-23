""" Module for obtaining information on Academic Records. """
# import os
import re
import sys
import getpass
import unicodedata

import click
import requests
from bs4 import BeautifulSoup


def cred_input():
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    secf = 'secrets.py'
    with open(secf, 'w') as f:
        f.write('USERNAME = \'{}\'\nPASSWORD = \'{}\'\n'.format(username, password))
    print('User credentials are now maintained in {0}.\n'.format(secf))
    # sys.exit(1)


try:
    from secrets import USERNAME, PASSWORD
    if not USERNAME or not PASSWORD:
        print('Please maintain your credentials.')
        cred_input()
except ImportError:
    cred_input()
    from secrets import USERNAME, PASSWORD


class Result(object):
    """ Class representing an academic record. """

    def __init__(self, semester, exam, grade, ects, passed):
        self.semester = semester
        self.exam = exam
        self.grade = grade
        self.ects = ects
        self.passed = passed

    def __str__(self):
        if self.passed:
            return '{:<14}{:<40} = {:>} ({} ECTS)'.format(self.semester, self.exam, self.grade, self.ects)
        else:
            return 'Not yet passed: {}'.format(self.exam)


class Student(object):

    def __init__(self):
        self.name = ''


class RecordHandler(object):
    """ Class for handling different functions regarding grades and exams. """

    MSC_ECTS = 120
    BSC_ECTS = 180

    def __init__(self, results):
        self.results = results

    def calc_gpa(self):
        sum_ects = 0
        sum_grade = 0
        for res in self.results:
            if res.passed:
                sum_grade += res.grade * res.ects
                sum_ects += res.ects
        return float(sum_grade / sum_ects)

    def print_exams(self):
        print(*self.results, sep='\n')


class Crawler(object):
    """ Class for crawling the information. """

    QIS_URL = 'https://portal.uni-mannheim.de/qisserver/rds?'
    CAS_URL = ('https://cas.uni-mannheim.de/cas/login?service='
               'https%3A%2F%2Fportal.uni-mannheim.de%2Fqisserver%2Frds%3Fstate%3Duser%26type%3D1')

    def __init__(self):
        self.session = requests.Session()

    def run(self):
        """ Main entry point. """
        self.login()
        results = self.parse_results()
        rec_handler = RecordHandler(results)
        # Print results
        gpa_str = 'Your GPA is: {0:.2f}'.format(rec_handler.calc_gpa())
        print('{}\n{}'.format(gpa_str, '-' * len(gpa_str)))
        rec_handler.print_exams()

    def login(self):
        """ Initialize session by logging in. """
        response = self.session.get(Crawler.CAS_URL)
        lt = re.findall('(LT-.*?)\"', response.text)[0]
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': 'Login'
        }
        self.session.post(Crawler.CAS_URL, data=payload, cookies=response.cookies)

    def parse_results(self):
        """ Navigate to 'Academic Records' and parse the results. """
        params = {
            'state': 'user',
            'type': '8',
            'topitem': 'pruefungen',
            'breadCrumbSource': 'portal'
        }
        response = self.session.get(Crawler.QIS_URL, params=params)
        try:
            soup_portal = BeautifulSoup(response.text, 'html.parser')
            res_link = soup_portal.find('a', href=True, text='Notenspiegel')['href']
        except TypeError as te:
            print(('{}\n\nA {} occurred while trying to access the website.\n'
                   'Make sure your credentials are correctly maintained.').format(te, te.__class__.__name__))
            sys.exit(1)

        response = self.session.get(res_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        elements = [tag.getText().strip() for tag in soup.find_all('th', {'class': 'Konto'})]
        no_elems = len(elements)

        raw_results = [self.strip(tag) for tag in soup.find_all('td', {'class': 'posrecords'})]
        res_tuples = list(self.group(raw_results, no_elems))
        results = []
        for tup in res_tuples:
            grade_lst = list(tup)
            semester = grade_lst[elements.index('Semester')]
            exam = grade_lst[elements.index('Prüfungsname')]
            grade = float(grade_lst[elements.index('Note')].replace(',', '.'))
            ects = int(self.parse_ects(grade_lst[elements.index('ECTS')]))
            passed = grade_lst[elements.index('Status')]
            results.append(Result(semester, exam, grade, ects, passed))
        return results

    def group(self, lst, n):
        """ Group given lst into tuples of size n. """
        for i in range(0, len(lst), n):
            values = lst[i:i + n]
            yield tuple(values)

    def strip(self, tag):
        """ Strip the tag and remove \xa0 """
        return unicodedata.normalize("NFKD", tag.getText().strip())

    def parse_ects(self, ectss):
        """ This is ugly but ECTS are decoded like this: (Example with 12 ECTS)
            <!-- document.write(Math.round(12.0*10)/10); //--> """
        return ectss.split('(')[2].split('.')[0]


@click.command()
def main():
    click.echo('Run!')
    print('Second')


if __name__ == '__main__':
    Crawler().run()
