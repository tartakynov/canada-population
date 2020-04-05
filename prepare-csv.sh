#!/usr/bin/env bash

axel --no-clobber https://download.geofabrik.de/north-america/canada-latest.osm.pbf --output=data/raw/

osmconvert data/raw/canada-latest.osm.pbf \
  --drop-ways \
  --drop-relations \
  --out-o5m > data/processed/canada-all-nodes.o5m

osmfilter data/processed/canada-all-nodes.o5m \
  --keep-nodes="place=city or place=town or place=village" \
  --out-o5m > data/processed/canada-settlements.o5m

osmconvert data/processed/canada-settlements.o5m \
  --all-to-nodes \
  --csv="@id @lon @lat place name population" \
  --csv-headline > data/processed/canada-settlements.csv
