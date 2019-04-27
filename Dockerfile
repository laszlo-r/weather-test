
FROM python:3.7-slim

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential python-dev python-pip

WORKDIR /home/weather
ADD . /home/weather
RUN pip install -r /home/weather/requirements.txt

CMD ["-p", "8000"]
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0"]
