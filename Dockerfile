FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt ; \
    chmod +x setup.sh ;
CMD bash setup.sh