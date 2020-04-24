# Nano On Tap
docker exec -it $(docker inspect --format="{{.Id}}" dg01) python manage.py createsuperuser
