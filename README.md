# This is a notification app / service

## Stack: 

- FastAPI
- SQLAlchemy
- PostgreSQL + Redis
- Celery+Rabbitmq

### Prerequisites

- Docker
- Git

### Installation & Setup

```git
git clone https://github.com/Kargozaur/notification_service
cd notification_service
```
After that, you'll need to create 2 .env files in the root folder(notification_service/)
.env_db looks like this 
```
db_password=<your_password_here>
db_name=<your_db_name>
db_user=<your_user_name>
```
And .env_rabbitmq
```
rabbitmq_user=<your_user_here>
rabbitmq_default_pass=<your_password_here>
rabbitmq_default_vhost=/
```
After that, you'll need to execute to create initial volumes
```
docker-compose --env-file .env_db --env-file .env_rabbitmq up -d
```
To stop the containers write
```
docker-compose --env-file .env_db --env-file .env_rabbitmq  down
```
We need those initial volumes to create a user for Celery. To do this, you need to perform:
```
docker exec -it notification_service-rabbitmq-1 rabbitmqctl add_user guest guest
docker exec -it notification_service-rabbitmq-1 rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
docker exec -it rabbitmq-1 rabbitmqctl set_user_tags guest administrator
```
After that, you need to add .env file inside /app/ folder. It contains:
```
DATABASE_URL=<your_db link, it may look like this: postgresql+asyncpg://<postgres_user>:<postgres_password>@127.0.0.1:5433/<db_name>
SECRET_KEY=<your_ssl_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REDIS_URL=redis://localhost:6379/0
RABBIT_MQ=amqp://guest:guest@127.0.0.1:5672//
TELEGRAM_TOKEN=<bot_token>
TELEGRAM_CHANNEL=<tg_channel_id>
```
To generate openssl key, write:
```
openssl rand -hex <your_length>
```
Data for the link DATABASE_URL is taken from .env_db.

To create a TG bot, generate token in the [BotFather](https://t.me/BotFather).

After that, add your bot to the group. To obrain channel id, you'll have to open TG Web, open your chat and in the url copy number after #. It may look like this
```
-1234567890
```

Now, when you're all set, start the docker containers.
After that, go down to the app folder (cd app) and perform:
```
uv sync
```
That should create a new virtual enviroment. Enter in it by:
```
source .venv/bin/activate
```
To create tables in the database(docker compose should be running):
```
alembic upgrade head
```
To start the app:
```
uvicorn main:app --host 0.0.0.0 --port 7000
```
After that, create second terminal, navigate to the app directory (cd app), activate venv if it's not activated and start the celery worker
```
celery -A tasks.app worker --pool=solo --loglevel=info
```
I'd recommend test it with Postman
```
base url: localhost:7000/
```
### User auth service
```
localhost:7000/auth/
```
Endpoints are: 
```
/signin - POST request
/login - POST request
```
To create a user you can something like this within the body request:
```
{
  "email": "user@example.com",
  "password": "<your password. 1 capital letter, 1 number, 1 special symbol>"
  "username": "<your username here>",
  "phone_number": "<international dummy number">
}
```
To login, you'll need to use email and a password. 
Add this script to automatically add JWT token in the environment:
```
pm.environment.set("JWT", pm.response.json().access_token)
```

### Notification service

Endpoints are:
```
/notifications - GET 
/notifications - PATCH
/notifications/notify - POST
```
PATCH request is based on [Pydantic model](/app/schemas/schemas.py) UpdateNotificationPref.

POST request is based on CreateNotification in the same file.

Make sure that you use telegram as your channel. Other channels are not supported currently.
