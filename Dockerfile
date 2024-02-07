from ubuntu:22.04

COPY main.py .
COPY requirements.txt .
copy asd.py .

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
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

CMD ["python3", "main.py"]


