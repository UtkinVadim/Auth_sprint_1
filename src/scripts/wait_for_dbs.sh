#!/usr/bin/env sh


until nc -z "$TEST_DB_HOST" "$TEST_DB_PORT"; do
  >&2 echo "Waiting for postgres..."
  sleep 1
done

until nc -z "$TEST_REDIS_HOST" "$TEST_REDIS_PORT"; do
  >&2 echo "Waiting for redis..."
  sleep 1
done

alembic upgrade head

exec "$@"
