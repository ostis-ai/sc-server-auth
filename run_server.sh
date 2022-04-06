#!/bin/bash

run_server()
{
  fi=${host:-127.0.0.1}
  fp=${port:-8000}
  pi=${platform_ip:-127.0.0.1}
  pp=${platform_port:-8090}
  python3 -m uvicorn main:app --reload --host "$fi" --port "$fp" 
}

help()
{
   echo "i     ip address of a flask server (default value is 127.0.0.1)"
   echo "p     port of a flask server (default value is 5000)"
   echo "s     ip address of a platform sc-server (default value is 127.0.0.1)"
   echo "c     port of a platform sc-server(default value is 8090)"
   echo ""
   echo "h     print this help"
   echo
}

while getopts "i:p:s:c:h" option; do
   case $option in
      i)
         host=$OPTARG;;
      p)
         port=$OPTARG;;
      s)
         platform_ip=$OPTARG;;
      c)
         platform_port=$OPTARG;;
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
