#!/bin/bash

source .env
export DB_NAME DB_USER DB_PASS DB_HOST DB_PORT REDIS_HOST REDIS_PORT

python3 manage.py runserver