#!/usr/bin/env bash
cd /usr/src/app
aerich init -t db.TORTOISE_ORM
aerich init-db

exec $@