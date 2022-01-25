FROM python:latest

ENV QT_QPA_PLATFORM=offscreen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential libglib2.0-dev netcat
RUN apt-get install -y xfonts-75dpi
RUN apt-get install -y xfonts-base
RUN apt-get install -y locales locales-all

WORKDIR /opt/

COPY lib lib
RUN dpkg --install /opt/lib/wkhtmltox_0.12.6-1.stretch_amd64.deb

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install pdfkit

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app app

RUN mkdir -p upload_files

COPY manager.py manager.py

#ENTRYPOINT ["/opt/init.sh"]

