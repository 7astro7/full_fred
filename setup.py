from setuptools import setup
from full_fred.constants import VERSION
import os

with open("README.md", encoding="utf-8") as readme:
    readme = readme.read()

setup(
    name="full_fred",
    packages=[
        "full_fred",
    ],
    version=VERSION,
    author="Zachary A. Kraehling",
    author_email="zaknyy@protonmail.com",
    description="Full interface to Federal Reserve Economic Data (FRED)",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=[],
    python_requires=">=3.8",
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
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="economics api econ fred FRED",
)
