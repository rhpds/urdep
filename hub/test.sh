#!/bin/sh

set -e

export DB_HOSTNAME=localhost
export DB_USERNAME=urdep
export DB_PASSWORD=urdep

if [[ "$1" == '--reset' ]]; then
    podman kill postgres &> /dev/null
    podman rm postgres &> /dev/null
    podman run --name postgres -e POSTGRES_USER=${DB_USERNAME} -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_DB=urdep -p 5432:5432 -d postgres &>/dev/null
    
    sleep 2
    
    rm -rf alembic/versions/*
    SKIP_TRIGGERS=true alembic revision --autogenerate -m 'initial'
    alembic upgrade head
    alembic revision --autogenerate -m 'triggers'
    alembic upgrade head
fi

URDEP_MODE=manager ./app.py &
sleep 1
export URDEP_MODE=api
exec ./app.py
