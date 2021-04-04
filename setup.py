
from setuptools import setup
import os

setup(
        name = 'full_fred',
        packages = ['full_fred',],
        version = '0.0.1.dev1',
        author = 'Zachary A. Kraehling',
        author_email = 'zaknyy@protonmail.com',
        description = 'Full interface to Federal Reserve Economic Data (FRED)',
        long_description = 'pass',
        license = 'GNU General Public License v3 (GPLv3)',
        install_requires = [],
        python_requires = '>=3.8',
        url = 'https://github.com/7astro7/full_fred',
        test_suite = 'full_fred.tests',
        platforms = ['Any'],
        classifiers = [
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Operating System :: Unix',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python :: 3.8',
            ], 
        )
