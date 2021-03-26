
from setuptools import setup
import os

path = os.path.join('new_fred', 'constants.py')
def get_version():
    version = None
    with open(path, 'r') as f:
        version = f.readlines()
    return version


setup(
        name = 'full_fred',
        packages = ['new_fred',],
        version = get_version(),
        author = 'Zachary A. Kraehling',
        author_email = 'zaknyy@protonmail.com',
        description = 'New, full interface to Federal Reserve Economic Data (FRED)',
        long_description = 'pass',
        LICENSE = 'GPLv3',
        install_requires = [],
        python_requires = '>=3.8',
        url = 'https://github.com/7astro7/full_fred',
        test_suite = 'tests.test_fred_class',
        platforms = ['Any'],
        classifiers = [
            'Development Status :: dev1',
            'Environment :: Console',
            'Programming Language :: Python :: 3.8',
            ], # add to this
        )
