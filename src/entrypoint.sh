#!/bin/sh

#echo "Do I run this code???"

set -ex

exec gunicorn -w 4 -b '0.0.0.0:5000' --access-logfile=- 'app:app'
