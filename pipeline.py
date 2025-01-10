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
import math
import subprocess
from dataclasses import dataclass


PYTHON_VERSIONS = ['3.9', '3.10', '3.11', '3.12', '3.13']
PYLINT_RATING_THRESHOLD = 7


def print_header(message: str, delimeter: str = '≈'):
    """Prints header"""
    message = f' {message} '
    message_l = math.floor((80 - len(message)) / 2)
    message_r = math.ceil((80 - len(message)) / 2)
    print()
    print(f'{delimeter*message_l}{message}{delimeter*message_r}')
    print()


def run_pytest(py_versions: list) -> tuple[str, int, str]:
    """Runs pytest using multiple python interpreters"""
    for py_version in py_versions:
        print_header(f'PYTEST (python{py_version})')

        # create venv with selected python interpreter
        status, _ = subprocess.getstatusoutput(
            f'python{py_version} -m venv venv{py_version}')
        if status != 0:
            print(f'Interpreter of python{py_version} is not exists')
            continue
        del status

        # install requirements
        status, _ = subprocess.getstatusoutput(
            f'./venv{py_version}/bin/python -m pip install -r requirements.txt')
        if status != 0:
            print(f'Can not install requirements on python{py_version}')
            subprocess.getstatusoutput(f'rm -rf venv{py_version}')
            continue
        del status

        # run pytest
        pytest_status, pytest_output = subprocess.getstatusoutput(
            f'./venv{py_version}/bin/python -m pytest --verbose --cov=connectionz')

        # remove temp files
        subprocess.getstatusoutput('rm .coverage')
        subprocess.getstatusoutput(f'rm -rf venv{py_version}')

        yield py_version, pytest_status, pytest_output


def run_pylint() -> tuple[float, str]:
    """Runs pylint"""
    print_header('PYLINT')

    pylint_output = subprocess.getoutput('pylint connectionz')

    pylint_rating = float(re.search(
        r'code\shas\sbeen\srated\sat\s(\d{1,2}\.?\d{1,2})\/10', pylint_output).group(1))

    return pylint_rating, pylint_output


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
    actual_license = first_line.replace('\n', '').replace('License', '').strip().replace(' ', '%20')

    return actual_license


@dataclass
class Badge:
    """Dataclass for badge parameters representation"""
    file_name: str
    subject: str
    value: str | int | float
    color: str


def download_badges(badges: list[Badge]):
    """Downloads badges"""
    print_header('BADGES')

    if not os.path.exists('documentation/images/badges'):
        os.makedirs('documentation/images/badges')

    for badge in badges:
        badge_url = f'https://badgen.net/badge/{badge.subject}/{badge.value}?color={badge.color}'
        badge_path = f'documentation/images/badges/{badge.file_name}'
        if os.path.exists(badge_path):
            os.remove(badge_path)

        status, _ = subprocess.getstatusoutput(f'wget -O {badge_path} "{badge_url}"')
        if status == 0:
            print(f'Badge {badge.file_name} downloaded')
        else:
            print(f'Error while downloading {badge.file_name}')


def main():
    """The main function"""
    py_versions = PYTHON_VERSIONS
    py_versions_passed = []
    for (py_version, pytest_status, pytest_output) in run_pytest(py_versions):
        if pytest_status == 0:
            py_versions_passed.append(py_version)
            print('Tests completed succesfully')
        else:
            print('Tests failed')
        if py_version == py_versions[-1]:
            print()
            print(pytest_output)
            if pytest_status != 0:
                sys.exit(1)
            print()

    pytest_total = int(re.search(r'=\s(\d{1,9})\spassed\sin[^=]+=', pytest_output).group(1))
    pytest_coverage = int(re.search(r'TOTAL.+\s(\d{1,3})%', pytest_output).group(1))

    if pytest_coverage >= 93:
        pytest_coverage_color = 'green'
    elif pytest_coverage >= 80:
        pytest_coverage_color = 'yellow'
    elif pytest_coverage >= 50:
        pytest_coverage_color = 'orange'
    else:
        pytest_coverage_color = 'red'

    print(f'Pytest total: {pytest_total}')
    print(f'Pytest coverage: {pytest_coverage}% ({pytest_coverage_color})')
    print(f'Python versions passed: {", ".join(py_versions_passed)}')

    pylint_rating, pylint_output = run_pylint()

    if pylint_rating >= 9.7:
        pylint_rating_color = 'green'
    elif pylint_rating >= 8.5:
        pylint_rating_color = 'yellow'
    elif pylint_rating >= 7:
        pylint_rating_color = 'orange'
    else:
        pylint_rating_color = 'red'

    print(pylint_output)
    # print()

    pylint_rating_threshold = PYLINT_RATING_THRESHOLD
    if pylint_rating < pylint_rating_threshold:
        print(f'Pylint failed: rating {pylint_rating} lower than {pylint_rating_threshold}')
        sys.exit(1)
    else:
        print(f'Pylint rating: {pylint_rating} ({pylint_rating_color})')

    actual_version = get_actual_version()

    actual_license = get_actual_license()

    badges = [
        Badge('pytest_total.svg', 'pytest', pytest_total, 'purple'),
        Badge('pytest_coverage.svg', 'coverage', f'{pytest_coverage}%', pytest_coverage_color),
        Badge('pylint_rating.svg', 'pylint', pylint_rating, pylint_rating_color),
        Badge('actual_version.svg', 'version', actual_version, 'blue'),
        Badge('actual_license.svg', 'license', actual_license, 'blue'),
        Badge('supported_python_versions.svg', 'python', ' | '.join(py_versions_passed), 'blue'),
    ]

    download_badges(badges)


if __name__ == '__main__':
    main()
