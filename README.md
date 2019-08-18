# arecs

A simple command line tool for retrieving your **a**cademic **rec**ord**s** from the University of Mannheim.

## Running the Program

These instructions will help you run the program.
You need to have pipenv installed.
```bash
$ pip3 install pipenv
```

Create a virtual environment and install the dependencies with pipenv:
```bash
$ pipenv install
```

To run the main program, you have to execute the script from within the `arecs/` folder in the repository:
```bash
$ cd arecs/
$ pipenv run python records.py
```

Enter your credentials in order to authenticate. With command line option `-s` your credentials will be stored (in plaintext) so you don't have to enter them again next time. Option `-m` will send an email to your university mail account if there are new records - this only works after the program has been run at least once. Run `--help` for more info on command line options.

```
$ pipenv run python records.py --help
Usage: records.py [OPTIONS]

Options:
  -s, --store  Store credentials (in plaintext). Can also be used to overwrite stored information.
  -m, --mail   Send an email if there are new records.
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

### Disclaimer

**Use this tool responsibly and at your own risk**. For example run it once a week with a cronjob on your RaspberryPi, but **do not** spam the university's servers by executing the program too frequently (which won't be beneficial anyways since your GPA doesn't change every other minute.). You are responsible for all consequences of your behavior. 