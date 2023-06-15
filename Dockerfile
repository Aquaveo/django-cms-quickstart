FROM python:3.9
WORKDIR /app
COPY . /app
# COPY docker-entrypoint.sh /docker-entrypoint.sh
# COPY checkdb.py /checkdb.py
RUN pip install -r requirements.txt ; \
    chmod +x setup.sh ;
# RUN python manage.py collectstatic --noinput
# CMD uwsgi --http=0.0.0.0:80 --module=backend.wsgi
CMD bash setup.sh