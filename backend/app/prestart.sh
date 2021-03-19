#!/usr/bin/env bash

# Let the DB start
python /app/scripts/backend_prestart.py

# Run migrations
alembic upgrade head