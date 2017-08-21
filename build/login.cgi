#!/bin/sh
# login.cgi-a cheery cgi page
printf "Content-type:text/plain\n\n";
python ./i/login.py $1
