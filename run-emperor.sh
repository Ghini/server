#!/bin/bash
cd /home/mario/Local/github/Ghini/server
. /home/mario/.virtualenvs/ghini/bin/activate
nohup uwsgi --emperor /home/mario/Local/github/Ghini/server/uwsgi.d/& 2>/dev/null
echo $! > emperor.pid
