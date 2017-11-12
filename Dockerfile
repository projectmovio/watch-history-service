FROM python:2.7

ADD . "/usr/local/src"
WORKDIR "/usr/local/src"

EXPOSE 5000

RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "run_flask.py"]
