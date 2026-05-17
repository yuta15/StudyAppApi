#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

psql \
    -v ON_ERROR_STOP=1 \
    -v POSTGRES_DB="$POSTGRES_DB" \
    -v DB_MIGRATION_USER="$DB_MIGRATION_USER" \
    -v DB_MIGRATION_PASSWORD="$DB_MIGRATION_PASSWORD" \
    -v DB_APP_USER="$DB_APP_USER" \
    -v DB_APP_PASSWORD="$DB_APP_PASSWORD" \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    --file "$script_dir/sql/initialize.sql"
