# arecs

A simple command line tool for retrieving your **a**cademic **rec**ord**s** from the University of Mannheim.

## Getting Started

These instructions will help you run the program.

### Prerequisites

What you need and how to install the prerequisites required for running the program. 

#### Pipenv

You need to have pipenv installed.

```bash
pip3 install pipenv
```

### Installing & Running

Create a virtual environment and install the dependencies with pipenv:

```bash
$ pipenv install
```

To run the main program, you have to execute the script from within the `arecs/` folder in the repository:

```bash
$ cd arecs/
$ pipenv run python records.py
```

Enter your credentials in order to access the server. With command line option `-s` your credentials will be stored (in plaintext) so you don't have to enter them again. Run `--help` for more info on command line options.

```bash
$ pipenv run python records.py --help
Usage: records.py [OPTIONS]

Options:
  -s, --store  Store credentials (in plaintext).
  --help       Show this message and exit.
```

The program will output your current GPA and display exam information.

Sample Output:

```
Hi Max (1234543)!
Degree: Business Informatics
Semester: 2
You have reached 18 ECTS so far.

Your GPA is: 1.67
-----------------
FSS 18       1.3   6 ECTS   CS 123 Machine Learning
FSS 18       1.7   6 ECTS   IE 234 Information Systems
FSS 18       2.0   6 ECTS   CS 443 Database Systems II
```

## Running the Tests

In order to run the tests, out of the `test/` directory run:

```bash
$ py.test
```

## Built With

* [Python](https://docs.python.org/3/) - Python 3.6
* [Pipenv](https://docs.pipenv.org/) - Python Development Workflow for Humans
* [Requests](http://docs.python-requests.org/en/master/) - HTTP requests library
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parser
* [Click](https://click.palletsprojects.com/en/7.x/) - Python CLI

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.