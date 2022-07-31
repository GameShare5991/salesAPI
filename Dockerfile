FROM python:3

WORKDIR /app

ADD salesapi.py .
ADD salesJSON .
ADD serviceAccountKey.json .

RUN python -m pip install --upgrade pip
RUN pip install wheel
RUN pip install flask

RUN pip install firebase-admin
RUN pip install Flask-Cors

EXPOSE 4005

CMD ["python", "salesapi.py"]