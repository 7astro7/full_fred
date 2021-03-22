
from setuptools import setup
import os

path = os.path.join('fredcli', 'constants.py')
def get_version():
    version = None
    with open(path, 'r') as f:
        version = f.readlines()
    return version


setup(
        name = 'fredcli',
        packages = ['fredcli',],
        entry_points = {
            'console_scripts': [
                'fredcli = fredcli.cli:main'
                ],
            },
        version = get_version(),
        author = 'Zachary A. Kraehling',
        author_email = 'zaknyy@protonmail.com',
        description = 'Command-line interface to Federal Reserve Economic Data (FRED) via fredapi',
        long_description = 'pass',
        LICENSE = 'GPLv3',
        install_requires = ['docopt', 'fredapi',],
        python_requires = '>=3.8',
        url = 'https://github.com/7astro7/fredcli',
        test_suite = 'tests.test_cli',
        platforms = ['Any'],
        classifiers = [
            'Development Status :: dev1',
            'Environment :: Console',
            'Programming Language :: Python :: 3.8',
            ], # add to this
        )
