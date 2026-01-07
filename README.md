docker-compose --env-file .env_db --env-file .env_rabbitmq up -d
docker-compose --env-file .env_db --env-file .env_rabbitmq  down
celery -A tasks.app worker --pool=solo --loglevel=info