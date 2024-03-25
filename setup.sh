#!/bin/bash -x


echo "$DJANGOCMS_ADMIN_DB_USER"
echo "$DJANGOCMS_ADMIN_DB_PWD"
if [ -z "${DJANGOCMS_DB_HOST}" ]; then
        export DJANGOCMS_DB_HOST='postgres'
else
        echo >&2 "  DJANGOCMS_DB_HOST  found"
        echo >&2 "  Connecting to DJANGOCMS_DB_HOST ($DJANGOCMS_DB_HOST)"
        echo >&2 "  instead of a postgres container"
fi


if [ -z "${DJANGOCMS_ADMIN_DB_USER}" ] && [ -z "${DJANGOCMS_ADMIN_DB_PWD}" ]; then
        export DJANGOCMS_ADMIN_DB_USER='postgres'
        export DJANGOCMS_ADMIN_DB_PWD=''
        echo >&2 "  this assumes the admin DJANGOCMS_ADMIN_DB_USER is postgres and the password is empty"
        echo >&2 "  this is a security hazard, kindly change"
        echo >&2 "  You may notice a password is not required when connecting from localhost (inside the same container)"
        echo >&2 "  this is becauseThe PostgreSQL image sets up trust authentication locally therefor  "
        echo >&2 "  a password will be required if connecting from a different host/container"
        echo >&2 "  Use -e POSTGRES_PASSWORD=password to set it in the docker run of your postgres db if its a container"
else
        echo >&2 "  DJANGOCMS_ADMIN_DB_USER ($DJANGOCMS_ADMIN_DB_USER) and DJANGOCMS_ADMIN_DB_USER found"
fi

if [ -z "${DJANGOCMS_ADMIN_DB_USER}" ]; then
        export DJANGOCMS_ADMIN_DB_USER='postgres'
        echo >&2 "  this assumes the admin DJANGOCMS_ADMIN_DB_USER is postgres "
else
        echo >&2 "  DJANGOCMS_ADMIN_DB_USER found"
fi

if [ -z "$DJANGOCMS_DB_PORT" ]; then
        export DJANGOCMS_DB_PORT=5432
else
        echo >&2 "  DJANGOCMS_DB_PORT found ($DJANGOCMS_DB_PORT)"
fi

# Ensure the MySQL Database is create

python checkdb.py "$DJANGOCMS_DB_HOST" "$DJANGOCMS_DB_NAME" "$DJANGOCMS_DB_USER" "$DJANGOCMS_DB_PWD" "$DJANGOCMS_DB_PORT" "$DJANGOCMS_ADMIN_DB_USER" "$DJANGOCMS_ADMIN_DB_PWD" 

echo >&2 "========================================================================"
echo >&2
echo >&2 "This server is now configured to run djangocms!"
echo >&2
echo >&2
echo >&2 "========================================================================"

# popualte settings.py template file

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py makemigrations backend
python manage.py migrate backend

python manage.py makemigrations zotero_publications_app
python manage.py migrate zotero_publications_app

python manage.py makemigrations hydrolearn_modules_app
python manage.py migrate hydrolearn_modules_app

python manage.py makemigrations hydroshare_resources_app
python manage.py migrate hydroshare_resources_app

if [ -z "${SKIP_CREATION_USER}" ]; then
        python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
fi
if [ -z "${INTERNAL_PORT_RUN}" ]; then
        echo >&2 "  INTERNAL_PORT_RUN not found running on port 80"
        python manage.py runserver 0.0.0.0:80
else
        echo >&2 "  INTERNAL_PORT_RUN found running on ${INTERNAL_PORT_RUN}"
        python manage.py runserver 0.0.0.0:${INTERNAL_PORT_RUN}
        # uwsgi --http=0.0.0.0:${INTERNAL_PORT_RUN} --module=backend.wsgi
fi