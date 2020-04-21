# Flights

Crawls real-time information on flights and airports.

## Usage

To crawl real-time flight information:
1. Run `python init_db.py` to initialize SQLite3 database;
2. Create `env.py` like `env.py.sample` and set values accordingly;
3. Edit `main.py` and set ICAO codes of airlines to be crawled;
4. Edit `flights.cron` as wished and copy into `/etc/cron.d/`.

To populate the airports table:
1. Run `python init_db.py` to initialize SQLite3 database;
2. Create `env.py` like `env.py.sample` and set values accordingly;
3. Run `python airports.py`.
