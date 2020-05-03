# Nano On Tap
## Overview
Nano On Tap is a stateless flow control and orchestration system for nano transactions. It introduces a 2nd layer ACL system to easily implement flow rules for the transfer of Nano from account to account within the system you design. It provides an API for programmatic interactions along with a UI for quick inspection and easy modeling.

Additionally flow state systems can be modeld, exported and imported through json templates. This allows for creation of complex use cases.

The core advantage of Nano On Tap TODO

### Simple Example

### Nano Poker Example

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
```sd
docker-compose build && docker-compose up -d
```
3. Check everything deployed. Go to http://localhost:8000/admin/. You should see a login screen.
![Login Screen](https://i.imgur.com/OFRk9Dg.png)
4. Create Django superuser
```sh
docker exec -it $(docker inspect --format="{{.Id}}" dg01) python manage.py createsuperuser
```
5. Import Nano Poker JSON template by sending a POST request `POST action/template/import` including the JSON in `poker_template.json` as the request bobdy. This imports and defines the Poker flow state.
```
POST action/template/import
```
6. Restart the docker container to bootstrap the Nano Wallet and Nano Accounts from Nano Node. This automaticlly creates a new wallet and needed accounts on the Node.

## Developer Usage

### Setup
TODO
