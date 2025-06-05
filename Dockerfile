FROM python:3.11

#Setting workdir
WORKDIR /app

#Installing FFmpeg
RUN apt-get update -qq && apt-get install ffmpeg -y

#Installing requirements
ADD src/requirements.txt .
RUN pip install -r requirements.txt

#Copying Gifski binaries
COPY bin/gifski-1_32_0 /usr/local/bin

#Setting Web enviroment variables
ENV FLASK_APP=/app/app.py
ENV FLASK_ENV=development
ENV PORT=80

#Exposing app.py port
EXPOSE 80

COPY src/ .

CMD flask run --host=0.0.0.0 -p 80 --debug
#CMD gunicorn -b :80 -w 8 app:app
