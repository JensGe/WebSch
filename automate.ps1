# Stop running docker containers
docker ps -q | % { docker stop $_ }

# pull latest dockerjens23/websch Image
docker pull dockerjens23/websch

# rebuild local container
docker build -t websch .

# run rebuilt container
docker run -d -p 80:80 websch

