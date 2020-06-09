#!/bin/bash

DOMAIN=ghini.me
BASEDIR=/home/mario/Local/github/Ghini/server/
VIRTUALENV=/home/mario/.virtualenvs/server/

grep uwsgi_pass /etc/nginx/sites-available/*.${DOMAIN} 2>/dev/null |
    sed -n -e "s@.*/sites-available/\([a-z0-9-]*\)\.${DOMAIN}:.*:\([0-9]*\);@\1:\2@p" |
    while IFS=':' read -ra i
    do
        SITE=${i[0]}
        PORT=${i[1]}
        cat > ${SITE}.ini << EOF
[uwsgi]
socket = 127.0.0.1:${PORT}
chdir = ${BASEDIR}
env = DJANGO_SETTINGS_MODULE=ghini.settings_${SITE}
virtualenv = ${VIRTUALENV}
wsgi-file = ghini/wsgi.py
processes = 4
threads = 2
EOF
    done
