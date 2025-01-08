#!venv/bin/python

"""Script that

- runs pytest
- runs pylint
- creates badges for readme

* we use badges from https://badgen.net/, thanks a lot to the developers for the
opportunity to use their product for free
"""

import os
import re
import sys
import subprocess
from dataclasses import dataclass


def get_pytest_report() -> tuple[int, int]:
    """Runs tests and returns tuple with number of tests in int and code
    coverage percent in int
    """
    print()
    print(f'{"-"*36} PYTEST {"-"*36}')
    print()
    status, output = subprocess.getstatusoutput('pytest --cov=connectionz --verbose')
    print(output)
    print()
    os.remove('.coverage')

    if status != 0:
        print('Tests were unsuccessful!')
        sys.exit(1)

    total = int(re.search(r'=\s(\d{1,9})\spassed\sin[^=]+=', output).group(1))
    coverage = int(re.search(r'TOTAL.+\s(\d{1,3})%', output).group(1))

    return total, coverage


def get_pylint_report() -> float:
    """Runs pylint and returns pylint rating in float"""

    print()
    print(f'{"-"*36} PYLINT {"-"*36}')
    print()
    output = subprocess.getoutput('pylint connectionz')
    print(output)

    rating = float(re.search(r'has\sbeen\srated\sat\s(\d{1,2}\.?\d{1,2})\/10', output).group(1))

    if rating < 7:
        print(f'Pylint rating is too low: {rating}/10!')
        sys.exit(1)

    return rating


def get_actual_version() -> str:
    """Returns actual package version"""
    output = subprocess.getoutput('git tag')

    tags = sorted(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}', output), reverse=True)
    actual_version = tags[0]

    return actual_version


def get_actual_license() -> str:
    """Returns actual license"""
    with open('LICENSE', 'r', encoding='utf-8') as file:
        first_line = file.readline()
    actual_license = first_line.replace('\n', '').replace(' ', '%20')

    return actual_license


def get_python_versions() -> list[str]:
    """Returns supported python versions"""
    return ['3.10', '3.11', '3.12', '3.13']


def main():
    """The main function"""
    pytest_total, pytest_coverage = get_pytest_report()
    if pytest_coverage >= 93:
        pytest_coverage_color = 'green'
    elif pytest_coverage >= 80:
        pytest_coverage_color = 'yellow'
    elif pytest_coverage >= 50:
        pytest_coverage_color = 'orange'
    else:
        pytest_coverage_color = 'red'

    pylint_rating = get_pylint_report()
    if pylint_rating >= 9.7:
        pylint_rating_color = 'green'
    elif pylint_rating >= 8.5:
        pylint_rating_color = 'yellow'
    elif pylint_rating >= 7:
        pylint_rating_color = 'orange'
    else:
        pylint_rating_color = 'red'

    actual_version = get_actual_version()

    actual_license = get_actual_license()

    python_versions = get_python_versions()

    print()
    print(f'{"-"*36} BADGES {"-"*36}')
    print()

    if not os.path.exists('documentation/images/badges'):
        os.makedirs('documentation/images/badges')

    @dataclass
    class Badge:
        """Dataclass for badge parameters representation"""
        file_name: str
        subject: str
        value: str | int | float
        color: str

    badges = [
        Badge('pytest_total.svg', 'pytest', pytest_total, 'purple'),
        Badge('pytest_coverage.svg', 'coverage', f'{pytest_coverage}%25', pytest_coverage_color),
        Badge('pylint_rating.svg', 'pylint', pylint_rating, pylint_rating_color),
        Badge('actual_version.svg', 'version', actual_version, 'blue'),
        Badge('actual_license.svg', 'license', actual_license, 'blue'),
        Badge('supported_python_versions.svg', 'python', '%20|%20'.join(python_versions), 'blue'),
    ]

    for badge in badges:
        status, _ = subprocess.getstatusoutput(
            (f'wget -O documentation/images/badges/{badge.file_name} '
             f'"https://badgen.net/badge/{badge.subject}/{badge.value}?color={badge.color}"'))
        if status == 0:
            print(f'Badge {badge.file_name} updated')

    print()


if __name__ == '__main__':
    main()
