# The line below states we will base our new image on the Latest Mintapi release
FROM ghcr.io/mintapi/mintapi:latest

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

# Install necessary python packages
RUN pip3 install -r requirements.txt

# Expose port 7889
EXPOSE 7889

# Command to start service
CMD python3 CherryStrap.py
