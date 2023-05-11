from setuptools import setup, find_packages

NAME = "paramikohelper"
VERSION = "0.1.2"
PYTHON_REQUIRES = ">=3.9.0"
INSTALL_REQUIRES = [
    "paramiko>=3.0.2",
]

AUTHOR = "tbshiki"
AUTHOR_EMAIL = "info@tbshiki.com"
URL = "https://github.com/tbshiki/" + NAME

setup(name=NAME, author=AUTHOR, author_email=AUTHOR_EMAIL, url=URL, version=VERSION, packages=find_packages())
