import math
import json
import sqlite3
import requests
from time import gmtime, strftime
from env import FLIGHTS_API, ACCESS_KEYS, PROXY


def request(access_key, airline, offset):

    # Specify API request parameters
    params = {
        "access_key": access_key,
        "airline_icao": airline,
        "limit": 100,
        "offset": offset
    }

    # Request the information
    response = requests.get(FLIGHTS_API, params, proxies=PROXY)

    return response.json(), response.url


def insert_into_db(cur, body):

    # If there is no data in the body then
    # raise an error.
    if not body.get("data"):
        raise Exception("No data found in response.")

    flights = flatten(body["data"])

    # Write flight information dictionaries to the
    # output file.
    cur.executemany("""
    INSERT INTO flights VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, flights)

    return None


def flatten(body_data):

    timestamp = strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime())

    flights = []
    for elem in body_data:

        if not isinstance(elem, dict):
            print("[ERROR] Element in body['data'] is not dict")
            continue

        dep = elem.get("departure", {})
        arr = elem.get("arrival", {})
        airline = elem.get("airline", {})
        flight = elem.get("flight", {})

        flight = (
            timestamp,
            elem.get("flight_date"),
            elem.get("flight_status"),
            dep.get("airport"),
            dep.get("icao"),
            dep.get("scheduled"),
            arr.get("airport"),
            arr.get("icao"),
            arr.get("scheduled"),
            airline.get("name"),
            airline.get("icao"),
            flight.get("iata"),
        )

        flights.append(flight)

    return flights


def main(airline):

    con = sqlite3.connect("db")
    cur = con.cursor()

    access_key = iter(ACCESS_KEYS)
    key = next(access_key)

    # Get an initial response to get information on the
    # amount of flights to be crawled, which is necessary
    # to pass in correct offset values
    body, url = request(key, airline, offset=0)

    # If the error code for an exhausted access key is given
    # take the next access key. If there are no more access
    # keys available, raise an error and exit the program
    if body.get("error", {}).get("code") == 104:
        try:
            key = next(access_key)
        except StopIteration:
            raise Exception("All access keys exhausted. Exiting.")

    # If another error occurs on the server side, print
    # print the error.
    elif body.get("error"):
        print(body["error"].get("info"))

    # Save the flights in the response from the initial
    # request.
    insert_into_db(cur, body)
    con.commit()

    # Calculate the amount of requests to be made to the endpoint
    # based on the number of flights in the pagination info
    n_requests = math.ceil(
        body["pagination"]["total"] / body["pagination"]["limit"]
    )

    c = 1
    while True:

        # If the succesful requests counter surpasses the number
        # of request to be made exit the while loop.
        if c == n_requests:
            break

        # Send request to the endpoint
        body, url = request(key, airline, offset=c * 100)

        # Check if the access key is exhausted and get a new one
        # if that is the case. In case all access keys are
        # exhausted exit the program.
        if body.get("error", {}).get("code") == 104:
            try:
                key = next(access_key)
                print(f'Key exhausted. Using "{key}".')
                continue
            except StopIteration:
                raise Exception("All access keys exhausted. Exiting.")

        # Save flight data in body and increment the successful
        # request counter.
        print(url)
        insert_into_db(cur, body)
        con.commit()
        c += 1

    con.close()

    return None


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--airline", type=str, help="IATA code of airline")
    args = parser.parse_args()

    main(airline=args.airline)
