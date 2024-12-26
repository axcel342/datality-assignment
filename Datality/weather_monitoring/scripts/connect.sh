#!/bin/bash

# Replace these variables with your TimescaleDB cloud credentials
TIMESCALE_HOST="tukgoycvpd.fgcmu7l9b7.tsdb.cloud.timescale.com"
TIMESCALE_PORT="30397"
TIMESCALE_DB="tsdb"
TIMESCALE_USER="tsdbadmin"
TIMESCALE_PASSWORD="x4gw2ogcfu0peh4w"

# Connection string
export PGPASSWORD=$TIMESCALE_PASSWORD

# Test connection
psql "host=$TIMESCALE_HOST port=$TIMESCALE_PORT dbname=$TIMESCALE_DB user=$TIMESCALE_USER sslmode=require"