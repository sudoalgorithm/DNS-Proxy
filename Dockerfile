FROM python:3.8-alpine
RUN pip install gunicorn
EXPOSE 53