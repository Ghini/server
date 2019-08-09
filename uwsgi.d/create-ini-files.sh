#!/bin/bash
for SITE in almaghreb caribe cuaderno cuchubo la-macarena paardebloem tanager
do
    PORT=$(grep uwsgi_pass /etc/nginx/sites-available/$SITE.ghini.me |
               while IFS=':' read -ra i
               do
                   echo ${i[1]} | tr -d ';'
               done
        )
    cat > $SITE.ini << EOF
[uwsgi]
socket = 127.0.0.1:${PORT}
chdir = /home/mario/Local/Ghini/server/
env = DJANGO_SETTINGS_MODULE=ghini.settings_${SITE}
module = django.core.handlers.wsgi:WSGIHandler()
processes = 4
threads = 2
EOF
done
