# Nano On Tap
## Overview
Nano On Tap is a stateless flow control and orchestration system for Nano transactions. It introduces a 2nd layer ACL system to easily implement flow rules for the transfer of Nano from account to account within the system you design. It provides an API for programmatic interactions along with a UI for quick inspection and easy modeling.

Additionally flow state systems can be modeled, exported and imported through json templates. This allows for creation of complex use cases with ease.

The core advantage of Nano On Tap is allowing any developer to quickly build and scale out a Nano based application. It reduces the need to deal in the details of transaction generation, proccessing, PoW mangement or manage business rules around where and how transaction should or can take place.

## Architecture
Nano On Tap uses small modular components to define complexy flow states. The below outlines the indiviual components and provides an example flow state system.

### Components
#### Application
An Application holds all objects defined in the system. One Nano On Tap backend can support multiple different applications.

#### Action Set
Each element has a priority and a list of Actions.
....


### Simple Example

For a complete and more complex read world example visit [Nano Poker - Play Nano with NFC stickers and readers](https://github.com/silverstar194/NanoPoker)

## Production
### Prerequisites
* Docker
* [Nano Node](https://docs.nano.org/running-a-node/node-setup/)
* [PoW Provider](https://nanocenter.org/projects/dpow) 

### Docker usage **RECOMMENDED**
The provided production stack is dockerized and includes:
* gunicorn (dg01 container)
* nginx (ng01 container)
* postgres (ps01 container)

The dockerized setup is meant to be used as a drop in backend. A admin UI is included for non-programic setup experience.

#### Setup
1. Clone NanoOnTap repo

```sh
git clone https://github.com/silverstar194/NanoOnTap.git
```
2. Create and start containers. Database will be created automatically.
```sh
docker-compose build && docker-compose up -d
```
3. Check everything deployed. Go to http://localhost:8000/admin/. You should see a login screen.
![Login Screen](https://i.imgur.com/OFRk9Dg.png)
4. Create Django superuser
```sh
docker exec -it $(docker inspect --format="{{.Id}}" dg01) python manage.py createsuperuser
```
5. You can now login and see flow state components.

## Developer Usage Setup
1. Clone NanoOnTap repo
```sh
git clone https://github.com/silverstar194/NanoOnTap.git
```

2. Install requirements 
```sh
 pip3 install config/requirements.pip 
```

3. Start development webserver
```sh
python3 backend/manage.py runserver
```

