#!/bin/sh

set -e

#if [ pwd != "/usr/src/app" ]
#then
#    cd /usr/src/app || exit
#fi

python manage.py collectstatic --noinput

exec "$@"