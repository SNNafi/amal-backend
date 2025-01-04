#!/bin/sh

if [ "$DATABASE" = "sqlite" ]
then
    echo "Waiting for SQLite..."

    echo "Creating the database directory..."
    mkdir -p /app/db

    echo "Making migrations..."
    python manage.py makemigrations
    
    echo "Applying migrations..."
    python manage.py migrate
fi

exec "$@"
