FROM python:2.7

WORKDIR /usr/src/app

COPY . /usr/src/app/

EXPOSE 12853

CMD ["python", "/usr/src/app/dns-over-tls-proxy.py"]