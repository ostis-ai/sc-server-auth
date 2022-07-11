#!/bin/bash

run_server()
{
  fi=${host:-127.0.0.1}
  fp=${port:-5000}
  python3 -m uvicorn sc_server_auth.main:app --reload --host "$fi" --port "$fp"
}

help()
{
   echo "i     ip address of a flask server (default value is 127.0.0.1)"
   echo "p     port of a flask server (default value is 5000)"
   echo ""
   echo "h     print this help"
   echo
}

while getopts "i:p:h" option; do
   case $option in
      i)
         host=$OPTARG;;
      p)
         port=$OPTARG;;
      h)
         help
         exit;;
      \?) # incorrect option
         echo "Error: Invalid option"
         help
         exit;;
   esac
  done

set -eo pipefail

run_server
