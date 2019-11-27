#!/usr/bin/env bash
echo 'starting MyhealthFlask project'
cd /usr/src/MyhealthFlask
git pull
pip install -r requirements.txt
cd /usr/src/MyhealthFlask/
gunicorn -w 1 -b 0.0.0.0:5000 -k gevent manage:application -D