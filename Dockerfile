FROM python:3.11 AS builder

# Setting workdir
WORKDIR /home/app

# Install FFmpeg
RUN apt-get -y update \
        && apt-get install -y --no-install-recommends ffmpeg  \
        && rm -rf /var/lib/apt/lists/*

# Copy Gifski binaries
COPY bin/gifski-1_32_0 /usr/local/bin

# Install requirements
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setting Web enviroment variable
ENV FLASK_APP=/home/app/app.py
COPY src/ .

# --target=debug
FROM builder AS dev
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "-p", "5000", "--debug"]

# --target=prod
FROM builder AS prod
ENV FLASK_ENV=production 
EXPOSE 80
CMD ["gunicorn", "-b", ":80", "-w", "8", "app:app"]
