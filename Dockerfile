FROM python:3.8-alpine
WORKDIR /usr/src/app
COPY . /usr/src/app/
EXPOSE 53
CMD ["python3", "/usr/src/app/dns-over-tls-proxy.py"]