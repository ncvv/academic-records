# arecs

A simple command line tool for retrieving your **a**cademic **rec**ord**s** from the University of Mannheim.

## Getting Started

These instructions will help you to run the tool.

### Prerequisites

What you need and how to install the prerequisites required for running the program. 

#### Pipenv

In order to install pipenv, the Python packaging tool wrapping virtualenv, you need to have Python3 and pip installed. Simply run:

```
pip3 install pipenv
```

### Installing

A step by step series of examples that tell you how to execute the program and to get a development env running.

Clone the git repo and create a virtual environment and install the dependencies with pipenv:

```
$ git clone https://www.github.com/ncvv/arecs.git
$ cd arecs/
$ pipenv install
```

You may now maintain your Uni Mannheim credentials in a file called `secrets.py` in order to access the server. You can create it yourself or run the program and it will create the file for you and you just have to fill in your credentials. The file should have the following format:

```
USERNAME='youruser'
PASSWORD='yourpw'
```

To run the main program, since we are now in a virtual environment created by pipenv, you have to:

```
$ pipenv run python arecs.py
```

For convenience, you may define a shell alias so you have to type only `prp` for running the program instead of typing `pipenv run python` everytime. If you are using the default shell (bash), for Linux you put it in `~/.bashrc`, for Mac in `~/.bash_profile`. This may vary for zsh or Fish or whatever shell you are using. Make sure you **use >>** instead of > in order to append the alias rather than overriding the file.

```
$ echo 'alias prp="pipenv run python"' >> ~/.bashrc
```

Finally, if you have maintained your credentials, you can calculate your current GPA and display exam information with

```
$ prp arecs.py
```

Sample Output:

Hi Max (1234543)!
Degree: Business Informatics
Semester: 2
You have reached 18 ECTS so far.

Your GPA is: 1.67
-----------------
FSS 18       1.3   6 ECTS   CS 123 Machine Learning
FSS 18       1.7   6 ECTS   IE 234 Information Systems
FSS 18       2.0   6 ECTS   CS 443 Database Systems II

## Running the Tests

How to run the tests

## Built With

* [Python](https://docs.python.org/3/) - Python 3.6
* [Requests](http://docs.python-requests.org/en/master/) - HTTP requests library
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parser

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.