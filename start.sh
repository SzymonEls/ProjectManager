#!/bin/bash

ENV_FILE=".env"
ENV_EXAMPLE_FILE=".env.example"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE_FILE" ]; then
        cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
    else
        exit 1
    fi
fi

#certbot certonly --standalone --non-interactive --agree-tos --keep-until-expiring --email contact@example.com -d example.com
#gunicorn --certfile=/etc/letsencrypt/live/example.com/fullchain.pem --keyfile=/etc/letsencrypt/live/example.com/privkey.pem -w 4 -b 0.0.0.0:8080 "app:create_app()" --preload

gunicorn -w 4 -b 0.0.0.0:8080 "app:create_app()" --preload