FROM python:3.11
COPY . /home
WORKDIR /home
RUN pip install --upgrade pip 
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y gcc make automake g++ subversion python3-dev gfortran musl-dev

RUN pip install -r requirements.txt --timeout 1000
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--timeout", "0", "index:server"]
