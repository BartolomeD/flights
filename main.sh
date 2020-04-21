#!/bin/bash
set -e
cd $HOME/flights/
for AIRLINE_ICAO in "dal" "ual" "aal" "klm"; do
    python flights.py --airline $AIRLINE_ICAO > flights.log 2>&1
done
