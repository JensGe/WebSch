# Stop running docker containers
docker ps -q | % { docker stop $_ }

# rebuild local container
docker build -t websch .

# run rebuilt container
docker run -d -p 80:80 websch

