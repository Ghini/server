#!/bin/bash

rm db.sqlite3
./manage.py migrate
./manage.py shell <<EOF
import desktop_reader
desktop_reader.do_import()
EOF
