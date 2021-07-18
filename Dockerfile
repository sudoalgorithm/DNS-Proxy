FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY . /usr/src/app/
EXPOSE 53
CMD ["python3", "/usr/src/app/proxy.py"]