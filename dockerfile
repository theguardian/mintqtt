# The line below states we will base our new image on the Latest Official Ubuntu
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=UTC

# Install important packages (git, python, etc)
RUN apt-get update && apt-get install python3.10 python3.10-dev python3.10-distutils python3-pip git gcc tzdata \
software-properties-common libmariadb-dev-compat libmariadb-dev pkg-config wget unzip -y

# Identify the maintainer of an image
LABEL maintainer="justin.evans@gmail.com"

# Establish base directory on image
WORKDIR /srv

# Clone mintqtt
RUN git clone https://github.com/theguardian/mintqtt

# Establish Workdir
WORKDIR /srv/mintqtt

# Make Chromium installable from deb (not snap)
RUN add-apt-repository ppa:saiarcot895/chromium-beta -y

# Now we can install Chromium without snap
RUN apt-get update && apt-get install chromium-browser -y

# amd64 only since arm64 chromedriver is hard to come by
RUN wget https://chromedriver.storage.googleapis.com/108.0.5359.22/chromedriver_linux64.zip
RUN mkdir chromedriver_tmp
RUN unzip chromedriver_linux64.zip -d chromedriver_tmp
RUN mv chromedriver_tmp/chromedriver /usr/lib/chromium-browser
RUN chmod +x /usr/lib/chromium-browser/chromedriver

# Have to add chromedriver to the PATH
ENV PATH "$PATH:/usr/lib/chromium-browser"

# Install necessary python packages
RUN pip3 install -r requirements.txt

# Expose port 7889
EXPOSE 7889

# Command to start service
CMD python3 CherryStrap.py
