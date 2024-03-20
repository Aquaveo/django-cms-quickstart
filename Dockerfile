FROM python:3.11
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt ; \
    chmod +x setup.sh ;
CMD bash setup.sh