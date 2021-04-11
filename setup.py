#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

with open('README.md', encoding='utf-8') as readme:
    readme = readme.read()

with open('full_fred/constants.py') as f:
    version = f.read().strip().split('=')[1].strip().replace('"', '')

INSTALL_REQUIRES = [
        'pandas', 
        'requests',
]

setup(
    name="full_fred",
    packages=find_packages(),
    version=version,
    description="Full interface to Federal Reserve Economic Data (FRED)",
    author="Zachary A. Kraehling",
    author_email="zaknyy@protonmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    url="https://github.com/7astro7/full_fred",
    project_urls={
        "Tracker": "https://github.com/7astro7/full_fred/issues",
        "Source": "https://github.com/7astro7/full_fred",
    },
    test_suite="full_fred.tests",
    platforms=["Any"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
    ],
    keywords=["economics", "API", "econ", "fred", "financial", "FRED",],
)
