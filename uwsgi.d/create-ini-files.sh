#!/bin/bash
#for SITE in almaghreb caribe cuaderno cuchubo la-macarena paardebloem tanager
for SITE in almaghreb cuaderno tanager paardebloem
do
    PORT=$(grep uwsgi_pass /etc/nginx/sites-available/$SITE.ghini.me 2>/dev/null |
               while IFS=':' read -ra i
               do
                   echo ${i[1]} | tr -d ';'
               done
        )
    [[ "$PORT" == "" ]] && continue
    cat > $SITE.ini << EOF
[uwsgi]
socket = 127.0.0.1:${PORT}
chdir = /home/mario/Local/github/Ghini/server/
env = DJANGO_SETTINGS_MODULE=ghini.settings_${SITE}
virtualenv = /home/mario/.virtualenvs/server/
wsgi-file = ghini/wsgi.py
processes = 4
threads = 2
EOF
done
