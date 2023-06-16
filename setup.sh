#!/bin/bash -x


set -e
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

        # If the DB user is 'root' then use the MySQL root password env var
        # : ${DJANGOCMS_DB_USER:=djangocms}
        # : ${DJANGOCMS_DB_PWD:=djangocms}
        # : ${DJANGOCMS_DB_NAME:=djangocms}

        # export DJANGOCMS_DB_USER DJANGOCMS_DB_PWD DJANGOCMS_DB_NAME


        # Ensure the MySQL Database is create

        # echo_status "Checking if DB is ready"

        # db_check_count=0
        # db_max_count=24;
        # until pg_isready -h ${DJANGOCMS_DB_HOST} -p ${DJANGOCMS_DB_PORT} -U postgres; do
        #         if [[ $db_check_count -gt $db_max_count ]]; then
        #                 >&2 echo "DB was not available in time - exiting"
        #                 exit 1
        #         fi
        #         >&2 echo "DB is unavailable - sleeping"
        #         db_check_count=`expr $db_check_count + 1`
        #         sleep 5
        # done

        python checkdb.py "$DJANGOCMS_DB_HOST" "$DJANGOCMS_DB_NAME" "$DJANGOCMS_DB_USER" "$DJANGOCMS_DB_PWD" "$DJANGOCMS_DB_PORT" "$DJANGOCMS_ADMIN_DB_USER" "$DJANGOCMS_ADMIN_DB_PWD" 

        echo >&2 "========================================================================"
        echo >&2
        echo >&2 "This server is now configured to run djangocms!"
        echo >&2
        echo >&2
        echo >&2 "========================================================================"

        # popualte settings.py template file

        # sed -i "s/mysite/$1/g" $1/settings.py
        python manage.py collectstatic --noinput
        python manage.py migrate
        if [ -z "${SKIP_CREATION_USER}" ]; then
                python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
        fi
        python manage.py runserver 0.0.0.0:80