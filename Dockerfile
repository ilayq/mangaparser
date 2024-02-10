from ubuntu:22.04

COPY main.py .
COPY requirements.txt .
copy asd.py .

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
run apt install software-properties-common -y
run add-apt-repository ppa:deadsnakes/ppa -y
run apt update -y
RUN echo 8 | apt install python3.11 -y
RUN apt install -y python3.11-pip
RUN python3.11 -m pip install -r requirements.txt
run apt-get install -y wget

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz # no way to use this shit
# selenium.common.exceptions.WebDriverException: Message: Process unexpectedly closed with status 255 
#xD
run tar -xzvf geckodriver-v0.34.0-linux64.tar.gz -C /usr/local/bin
run chmod +x /usr/local/bin/geckodriver
RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*


ENV sender=$sender
ENV target=$target
ENV pwd=$pwd

CMD ["python3.11", "main.py"]

