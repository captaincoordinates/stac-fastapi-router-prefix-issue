#!/bin/bash

set -e

CONN_STRING="postgresql://$POSTGRES_USER:$POSTGRES_PASS@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DBNAME"

echo "loading STAC collections"
for COLLECTION_PATH in $COLLECTIONS_DIR/*.json; do
    pypgstac load collections $COLLECTION_PATH --method=upsert --dsn=$CONN_STRING
done

echo "loading STAC items"
for ITEM_PATH in $ITEMS_DIR/*.json; do
    pypgstac load items $ITEM_PATH --method=upsert --dsn=$CONN_STRING
done

echo "loaded successfully"
