#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def get_port_from_settings(default):
    try:
        import re
        pattern = re.compile(r'^(RUNSERVER_PORT)[ ]*=[ ]*([^#]*)')
        import sys
        index = sys.argv.index('--settings')
        module_name = sys.argv[index + 1]
        file_name = module_name.replace('.', '/') + '.py'
        with open(file_name) as f:
            for line in f.readlines():
                line = line.strip()
                match = pattern.match(line)
                if not match:
                    continue
                return int(match.group(2))
    except Exception as e:
        return default


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghini.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = get_port_from_settings(8080)
    runserver.default_addr = '127.0.0.1'
    main()
