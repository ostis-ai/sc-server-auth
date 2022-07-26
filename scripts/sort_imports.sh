#!/bin/bash

isort() {
  poetry run isort -l 120 sc_server_auth/
}

black() {
  poetry run black -l 120 sc_server_auth/
}

help() {
  echo "usage: ./scripts/sort_imports.sh [-h] [-i] [-b] [-a]"
  echo
  echo "Sort imports and clean code tool"
  echo
  echo "optional arguments:"
  echo "  -h     Print this help"
  echo "  -i     Run isort"
  echo "  -b     Run black"
  echo "  -a     Run all sorters"
  echo
}

if [ $# -lt 1 ]; then
  help
  exit 0
fi

while getopts "ibah" option; do
  case $option in
  i)
    isort
    ;;
  b)
    black
    ;;
  a)
    isort
    black
    ;;
  h)
    help
    ;;
  \?)
    echo "Error: Invalid option"
    help
    exit
    ;;
  esac
done
