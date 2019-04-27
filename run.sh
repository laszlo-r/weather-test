
if [[ ! `docker images weather-test -q` ]]; then
	docker build -t weather-test .
fi

docker rm -f weather
docker run -h weather --name weather -p 8000:8000 -d weather-test

docker ps -l
