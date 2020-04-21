import sqlite3

con = sqlite3.connect("db")
cur = con.cursor()

cur.execute("""
CREATE TABLE flights (
    timestamp TIMESTAMP_NTZ,
    flight_date DATE,
    flight_status VARCHAR(9),
    dep_airport VARCHAR(255),
    dep_icao VARCHAR(4),
    dep_scheduled TIMESTAMP_NTZ,
    arr_airport VARCHAR(255),
    arr_icao VARCHAR(4),
    arr_scheduled TIMESTAMP_NTZ,
    airline_name VARCHAR(255),
    airline_icao VARCHAR(3),
    flight_number VARCHAR(255)
)
""")

cur.execute("""
CREATE TABLE airports (
    timestamp TIMESTAMP_NTZ,
    name VARCHAR(255),
    icao VARCHAR(4),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country_name VARCHAR(255),
    country_iso2 VARCHAR(2)
)
""")

con.close()
