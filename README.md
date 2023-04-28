# Brine-Crypto-Price-Alerts

*[Problem Statement](https://drive.google.com/file/d/1ZMqYGbMaciTpEia9YM1WCQVoIxHCcKxM/view?usp=share_link)
(Restricted as this is an interview exercise)*


## Setup Instructions

### Step 1

Install Docker: https://docs.docker.com/engine/install/

### Step 2

Clone this repository and `cd` into the `Brine-Crypto-Price-Alerts` folder in a terminal

### Step 3

Run the containers
```
docker-compose up -d
```

### Step 4

Bash into the django container and enter django shell
```
docker exec -it crypto-alerts-django bash
python manage.py shell
```

### Step 5
**Seed Data**

Copy the contents of `Brine-Crypto-Price-Alerts/seed_data.py` and paste and execute it in django shell

You now have 2 users with usernames `alertsuser001` and `alertsuser001`. Password for both these users is `password`

Each of these users have subscribed to some alerts. You may view these in the admin dashboard.


## View Triggered Alerts

Triggered alerts are logged in the docker logs `crypto-alerts-celery` Container

```
docker logs crypto-alerts-celery
```

## Admin Dashboard

You may enter the admin dashboard using the following information

**URL:** `http://localhost:8000/admin/`

**Username:** `admin`

**Password:** `admin`


## Postman collection

Download and install Postman: https://www.postman.com/downloads/

This repository also contains a postman collection JSON file for the APIs supported by the app

`Brine-Crypto-Price-Alerts/BrineCryptoPriceAlerts.postman_collection.json`

Each request also has a description and examples for easy understanding
