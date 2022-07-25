#!/bin/bash

unittest() {
  echo "--------------------------------------UNITTEST--------------------------------------"
  TEST_FLAG=true poetry run coverage run -m unittest discover -p "*_tests.py" -v -s sc_server_auth
  echo "------------------------------------------------------------------------------------"
}

coverage() {
  COVERAGE_LIMIT=90
  echo "--------------------------------------COVERAGE--------------------------------------"
  poetry run coverage report --fail-under=$COVERAGE_LIMIT -m
  echo "------------------------------------------------------------------------------------"
}

isort() {
  echo "--------------------------------------ISORT--------------------------------------"
  poetry run isort sc_server_auth --check --diff --line-length 120
  echo "---------------------------------------------------------------------------------"

}

black() {
  echo "--------------------------------------BLACK--------------------------------------"
  poetry run black --diff --color --line-length 120 .
  echo "---------------------------------------------------------------------------------"
}

pylint() {
  echo "--------------------------------------PYLINT--------------------------------------"
  poetry run pylint sc_server_auth
  echo "----------------------------------------------------------------------------------"
}

help() {
   echo "usage: ./scripts/local_ci.sh [-h] [-t] [-c] [-b] [-p] [-a]"
   echo
   echo "Local-CI is a special tool to check your code before pushing"
   echo
   echo "options:"
   echo "t     Run unittest"
   echo "c     Run coverage utility"
   echo "i     Run isort"
   echo "b     Run black"
   echo "p     Run pylint"
   echo "a     Run all checks"
   echo "h     Print this help"
   echo
}

if [ $# -lt 1 ]
then
  echo "No options found!"
  exit 1
fi

while getopts "tcibpah" option; do
   case $option in
      t)
         unittest;;
      c)
         coverage;;
      i)
         isort;;
      b)
         black;;
      p)
         pylint;;
      a)
         unittest
         coverage
         isort
         black
         pylint;;
      h) # display Help
         help
         exit;;
      \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
   esac
done
