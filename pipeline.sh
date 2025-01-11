#!/bin/bash

# script that
# - runs pytest using multiple python interpreters and get information about number of tests and code coverage percent
# - runs pylint and get pylint rating
# - gets actual project version and actual license
# - downloads badges from badgen.net

# exit codes explanation
# - exit code 1 = tests failed using latest python version
# - exit code 2 = pylint rating is too low
# - exit code 3 = error downloading badges

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# print header
function printheader() {
    PLACEHOLDER="~"

    MESSAGE=$(echo " $1 ")

    MESSAGE_LEN=${#MESSAGE}

    SPACE=$(expr "80" - "$MESSAGE_LEN")
    SPACE_L=$(expr "$SPACE" / "2")
    SPACE_R=$(expr $(expr "$SPACE" / "2") + $(expr "$SPACE" % "2"))

    MESSAGE_L=$(printf "$PLACEHOLDER%.0s" $(seq 1 $SPACE_L))
    MESSAGE_R=$(printf "$PLACEHOLDER%.0s" $(seq 1 $SPACE_R))

    echo
    echo "$MESSAGE_L$MESSAGE$MESSAGE_R"
    echo
}

# cleanup on exit
function cleanup() {
    echo
    echo "Clean up before exiting..."

    rm -rf ./venv3.* > /dev/null 2>&1
    rm .coverage > /dev/null 2>&1
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PREPARATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

trap cleanup EXIT

mkdir ./reports > /dev/null 2>&1
rm ./reports/*.txt > /dev/null 2>&1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PYTEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PY_VERSIONS=("3.9" "3.10" "3.11" "3.12" "3.13")
PY_V_LATEST="${PY_VERSIONS[@]:(-1)}"
PY_VERSIONS_PASSED=()

for PY_V in ${PY_VERSIONS[*]}; do
    printheader "PYTEST (python$PY_V)"

    # creating environment
    ~/.python$PY_V/bin/python$PY_V -m venv venv$PY_V > /dev/null
    environment_status_code=$?
    if [[ "$environment_status_code" != "0" ]]; then
        echo "Something went wrong while creating environment using python$PY_V"
        continue
    fi

    # installing dependencies
    ./venv$PY_V/bin/python -m pip install --upgrade pip > /dev/null
    ./venv$PY_V/bin/python -m pip install -r requirements.txt > /dev/null

    # running pytest
    ./venv$PY_V/bin/python -m pytest > /dev/null 2>&1
    tests_status_code=$?

    if [[ "$tests_status_code" == "0" ]]; then
        PY_VERSIONS_PASSED+=($PY_V)
        echo "Tests passed using python$PY_V"
    else
        echo "Tests failed using python$PY_V"
    fi

    if [[ "$PY_V" == "${PY_VERSIONS[@]:(-1)}" ]]; then
        echo
        ./venv$PY_V/bin/python -m pytest --verbose --cov=connectionz | tee ./reports/report_pytest_python$PY_V.txt
        echo
    else
        ./venv$PY_V/bin/python -m pytest --verbose --cov=connectionz > ./reports/report_pytest_python$PY_V.txt
    fi
done

if [[ ! " ${PY_VERSIONS_PASSED[*]} " =~ [[:space:]]${PY_V_LATEST}[[:space:]] ]]; then
    echo "Tests failed using latest python version (python$PY_V_LATEST)"
    exit 1
else
    # getting pytest total
    PYTEST_TOTAL=$(grep -Po "=\s\d{1,9}\spassed\sin[^=]+=" ./reports/report_pytest_python$PY_V_LATEST.txt | grep -Po "\s\d{1,9}\spassed\s" | grep -Po "\d+")
    echo "Pytest total: $PYTEST_TOTAL"

    # getting pytest coverage and calculating pytest coverage badge color
    PYTEST_COVERAGE=$(grep -Po "TOTAL.+\s\d{1,3}%" ./reports/report_pytest_python3.13.txt | grep -Po "\d{1,3}%" | grep -Po "\d+" | xargs printf "%0.0f\n")

    if (( $PYTEST_COVERAGE >= 93 )); then
        PYTEST_COVERAGE_COLOR="green"
    elif (( $PYTEST_COVERAGE >= 80 )); then
        PYTEST_COVERAGE_COLOR="yellow"
    elif (( $PYTEST_COVERAGE >= 50 )); then
        PYTEST_COVERAGE_COLOR="orange"
    else
        PYTEST_COVERAGE_COLOR="red"
    fi

    echo "Pytest coverage: $PYTEST_COVERAGE% ($PYTEST_COVERAGE_COLOR)"

    # getting python versions passed
    PY_VERSIONS_PASSED_STR="${PY_VERSIONS_PASSED[*]}"
    PY_VERSIONS_PASSED_STR_COMMA="${PY_VERSIONS_PASSED_STR// /, }"
    PY_VERSIONS_PASSED_STR_VBAR="${PY_VERSIONS_PASSED_STR// / | }"

    echo "Python versions passed: $PY_VERSIONS_PASSED_STR_COMMA"
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PYLINT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

printheader "PYLINT"

# running pylint
./venv$PY_V_LATEST/bin/python -m pylint connectionz | tee ./reports/report_pylint.txt

# getting pylint rating and calculating pylint rating badge color
PYLINT_RATING=$(grep -Po "code\shas\sbeen\srated\sat\s\d{1,2}\.?\d{0,2}\/10" reports/report_pylint.txt | grep -Po "\d{1,2}\.?\d{0,2}" | head -n 1  | xargs printf "%0.1f\n")

if (( $(echo "$PYLINT_RATING >= 9.9" | bc -l) )); then
    PYLINT_RATING_COLOR="green"
elif (( $(echo "$PYLINT_RATING >= 8.8" | bc -l) )); then
    PYLINT_RATING_COLOR="yellow"
elif (( $(echo "$PYLINT_RATING >= 7.7" | bc -l) )); then
    PYLINT_RATING_COLOR="orange"
else
    echo "Pylint rating is too low ($PYLINT_RATING), fix this"
    exit 2
    PYLINT_RATING_COLOR="red"
fi

echo "Pylint rating: $PYLINT_RATING ($PYLINT_RATING_COLOR)"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OTHER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# getting actual project version

printheader "VERSION"

ACTUAL_VERSION=$(git tag | grep -Po "\d\.\d\.\d" | sort -r | head -n 1)

echo "Actual project version is $ACTUAL_VERSION"

# getting project license

printheader "LICENSE"

ACTUAL_LICENSE=$(head -n 1 LICENSE)

echo "Project is distributed with the $ACTUAL_LICENSE"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BADGES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

printheader "BADGES"

mkdir ./documentation/images/badges > /dev/null 2>&1

# downloading badges from https://badgen.net/, thanks a lot to the developers for the opportunity to use their product for free

wget -q -O ./documentation/images/badges/pytest_total.svg "https://badgen.net/badge/pytest/$PYTEST_TOTAL?color=purple"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge pytest_total.svg downloaded"
else
    echo "Something went wrong while downloading badge pytest_total.svg"
    exit 3
fi

wget -q -O ./documentation/images/badges/pytest_coverage.svg "https://badgen.net/badge/coverage/$PYTEST_COVERAGE%?color=$PYTEST_COVERAGE_COLOR"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge pytest_coverage.svg downloaded"
else
    echo "Something went wrong while downloading badge pytest_coverage.svg"
    exit 3
fi

wget -q -O ./documentation/images/badges/pylint_rating.svg "https://badgen.net/badge/pylint/$PYLINT_RATING?color=$PYLINT_RATING_COLOR"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge pylint_rating.svg downloaded"
else
    echo "Something went wrong while downloading badge pylint_rating.svg"
    exit 3
fi

wget -q -O ./documentation/images/badges/actual_version.svg "https://badgen.net/badge/version/$ACTUAL_VERSION?color=blue"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge actual_version.svg downloaded"
else
    echo "Something went wrong while downloading badge actual_version.svg"
    exit 3
fi

wget -q -O ./documentation/images/badges/actual_license.svg "https://badgen.net/badge/license/$ACTUAL_LICENSE?color=blue"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge actual_license.svg downloaded"
else
    echo "Something went wrong while downloading badge actual_license.svg"
    exit 3
fi

wget -q -O ./documentation/images/badges/supported_python_versions.svg "https://badgen.net/badge/python/$PY_VERSIONS_PASSED_STR_VBAR?color=blue"
badge_download_status_code=$?
if [[ "$badge_download_status_code" == "0" ]]; then
    echo "Badge supported_python_versions.svg downloaded"
else
    echo "Something went wrong while downloading badge supported_python_versions.svg"
    exit 3
fi
