"""Module for obtaining information on Academic Records."""

import os
import re
import sys
import getpass
import unicodedata

import pickle
import click
import requests
from bs4 import BeautifulSoup


class Result(object):
    """Class representing an academic record."""
    def __init__(self, semester, exam, grade, ects, passed):
        self.semester = semester
        self.exam = exam
        self.grade = grade
        self.ects = ects
        self.passed = passed

    def __eq__(self, other):
        if not isinstance(other, Result):
            return NotImplemented

        return self.semester == other.semester \
            and self.exam == other.exam \
            and self.grade == other.grade \
            and self.ects == other.ects \
            and self.passed == other.passed

    def __hash__(self):
        return hash((self.semester, self.exam, self.grade, self.ects, self.passed))

    def __str__(self):
        if self.passed:
            return '{:<13}{}{:>4} ECTS   {}'.format(self.semester, self.grade, self.ects,
                                                    self.exam)
        else:
            return 'Not yet passed: ' + self.exam


class Student(object):
    """Class representing a student."""
    MSC_ECTS = 120
    BSC_ECTS = 180

    def __init__(self, name, matnr, degree, semester):
        self.name = name
        self.matnr = matnr
        self.degree = degree
        self.semester = semester
        self.gpa = 0.0
        self.sum_ects = 0
        self.missing_ects = 0

    def __str__(self):
        dashes = '-' * len('Your GPA is: {:.2f}'.format(self.gpa))
        return ('Hi {} ({})!\n'
                'Degree: \033[1m{}\033[0m\n'
                'Semester: \033[1m{}\033[0m\n'
                'You have reached \033[1m{}\033[0m ECTS so far.\n\n'
                'Your GPA is: \033[1m{:.2f}\033[0m\n{}').format(self.name, self.matnr, self.degree,
                                                                self.semester, self.sum_ects,
                                                                self.gpa, dashes)


class RecordHandler(object):
    """Class for handling different functions regarding grades and exams for a particular student."""
    def __init__(self, results, student):
        self.results = results
        self.student = student

    def calc_gpa(self):
        sum_ects = 0
        sum_grade = 0
        for res in self.results:
            if res.passed:
                sum_grade += res.grade * res.ects
                sum_ects += res.ects
        self.student.sum_ects = sum_ects
        self.student.gpa = float(sum_grade / sum_ects)

    def print_exams(self, new=None):
        print()
        print(self.student)
        # No difference compared to last run, simply print results
        if new is None:
            print(*self.results, sep='\n')
        # Highlight new records that have not been crawled in the last run
        else:
            for r in self.results:
                if r in new:
                    r = '\033[1m\033[31m{}\033[0m'.format(r)  # red
                print(r)


class Crawler(object):
    """Class for crawling the information."""
    QIS_URL = 'https://portal.uni-mannheim.de/qisserver/rds?'
    CAS_URL = ('https://cas.uni-mannheim.de/cas/login?service='
               'https%3A%2F%2Fportal.uni-mannheim.de%2Fqisserver%2Frds%3Fstate%3Duser%26type%3D1')

    RESULT_FILE = '.results'

    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def run(self):
        """Main entry point."""
        self.login()
        html = self.get_source()
        results, student = self.parse_results(html)
        new = self.diff(results)

        rec_handler = RecordHandler(results, student)
        rec_handler.calc_gpa()
        rec_handler.print_exams(new)

    def login(self):
        """Initialize session by logging in."""
        response = self.session.get(Crawler.CAS_URL)
        lt = re.findall('(LT-.*?)\"', response.text)[0]
        payload = {
            'username': self.username,
            'password': self.password,
            'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': 'Login'
        }
        self.session.post(Crawler.CAS_URL, data=payload, cookies=response.cookies)

    def get_source(self):
        """Navigate to 'Academic Records' section and return the html source."""
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
            print(te)
            print(
                '\n', te.__class__.__name__,
                ' occurred while trying to access the website. Make sure you entered correct credentials.'
            )
            sys.exit(1)

        response = self.session.get(res_link)
        return response.text

    def parse_results(self, html):
        """Parse the academic records from the html source."""
        soup = BeautifulSoup(html, 'html.parser')

        info = [tag.getText().strip() for tag in soup.find_all('span', {'class': 'nobr'})]
        name, matnr, degree, semester = info[1], info[3], info[5], info[7]
        student = Student(name, matnr, degree, semester)

        elements = [tag.getText().strip() for tag in soup.find_all('th', {'class': 'Konto'})]
        no_elems = len(elements)

        raw_results = [strip_unicode(tag.getText()) for tag in soup.find_all('td', {'class': 'posrecords'})]
        res_tuples = list(group(raw_results, no_elems))
        results = []
        for tup in res_tuples:
            grade_lst = list(tup)
            seme = grade_lst[elements.index('Semester')]
            exam = grade_lst[elements.index('Prüfungsname')]
            grad = float(grade_lst[elements.index('Note')].replace(',', '.'))
            ects = int(parse_ects(grade_lst[elements.index('ECTS')]))
            pasd = grade_lst[elements.index('Status')]
            results.append(Result(seme, exam, grad, ects, pasd))
        return results, student

    def diff(self, results):
        """Determine the difference between this run
           and last runs retrieved records."""
        if os.path.exists(Crawler.RESULT_FILE):
            # Deserialize
            with open(Crawler.RESULT_FILE, 'rb') as fp:
                old_results = pickle.load(fp)
            if len(old_results) == len(results):
                return None
            s = set(old_results)
            new = [r for r in results if r not in s]
            return new
        # Serialize
        with open(Crawler.RESULT_FILE, 'wb') as fp:
            pickle.dump(results, fp)


def group(lst, n):
    """Group given lst into tuples of size n."""
    for i in range(0, len(lst), n):
        values = lst[i:i + n]
        yield tuple(values)


def strip_unicode(tag):
    """Strip the given tag and remove unicode elements."""
    return unicodedata.normalize("NFKD", tag.strip())


def parse_ects(ectsstr):
    """This is ugly but ECTS are encoded like this: (Example with 12 ECTS)
       <!-- document.write(Math.round(12.0*10)/10); //-->."""
    return ectsstr.split('(')[2].split('.')[0]


@click.command()
@click.option('--store', '-s', is_flag=True, help="Store credentials (in plaintext).")
def cli(store):
    try:
        from secrets import USERNAME, PASSWORD
        if store:
            raise ImportError  # pretend nothing was stored in order to overwrite
    except ImportError:
        USERNAME = input('Username: ')
        PASSWORD = getpass.getpass('Password: ')
    if store:
        secfile = 'secrets.py'
        with open(secfile, 'w') as f:
            f.write('USERNAME = \'{}\'\n' 'PASSWORD = \'{}\'\n'.format(USERNAME, PASSWORD))
        print('Your credentials are stored in {} (as plaintext).'.format(secfile))

    crawler = Crawler(USERNAME, PASSWORD)
    try:
        crawler.run()
    except KeyboardInterrupt:
        print('Received KeyboardInterrupt, Terminating...')


if __name__ == '__main__':
    cli()
