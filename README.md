# Nano On Tap
## Development
### Setup
TODO

## Production
### Docker usage
TODO
Create Django Superuser
```sh
docker exec -it $(docker inspect --format="{{.Id}}" dg01) python manage.py createsuperuser
```
