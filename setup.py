from setuptools import setup

requires = ('fredapi',)

setup(
        name = 'fredcli',
        version = '0.01',
        url = 'https://github.com/7astro7/fredcli',
        author = 'Zachary A. Kraehling',
        author_email = 'zaknyy@protonmail.com',
        description = 'Command-line interface to Federal Reserve Economic Data (FRED) via fredapi',
        long_description = 'pass',
        test_suite = 'fredcli.tests.test_cli',
        packages = ('fredcli'),
        platforms = ['Any'],
        install_requires = requires,
        classifiers = [
            'Development Status :: ',
            ],
        )
