import requests
from datetime import datetime, timezone
from google.transit import gtfs_realtime_pb2

FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"

# Roosevelt Island
STATION_NAME = "Roosevelt Island (F)"

STOPS = {
    "Manhattan/Brooklyn": "B06S",
    "Queens": "B06N"
}


def fetch_feed():
    response = requests.get(FEED_URL)
    response.raise_for_status()
    return response.content


def parse_feed(feed_bytes):
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_bytes)
    return feed


def minutes_until(timestamp):
    now = datetime.now(timezone.utc)
    arrival = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    delta = arrival - now
    return int(delta.total_seconds() / 60)


def get_arrivals(feed, stop_id, limit=3):
    arrivals = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip = entity.trip_update

        # Filter only F trains
        if trip.trip.route_id != "F":
            continue

        for stu in trip.stop_time_update:
            if stu.stop_id == stop_id and stu.HasField("arrival"):
                mins = minutes_until(stu.arrival.time)

                if 0 <= mins <= 60:  # ignore past + far future
                    arrivals.append(mins)

    return sorted(arrivals)[:limit]


def main():
    print(f"\n🚇 {STATION_NAME}")
    print("=" * 30)

    feed_bytes = fetch_feed()
    feed = parse_feed(feed_bytes)

    for direction, stop_id in STOPS.items():
        arrivals = get_arrivals(feed, stop_id)

        print(f"\n{direction}:")

        if arrivals:
            for m in arrivals:
                print(f"  • {m} min")
        else:
            print("  No upcoming trains")

###
def get_arrivals_for_display():
    feed_bytes = fetch_feed()
    feed = parse_feed(feed_bytes)

    queens = get_arrivals(feed, "B06N", limit=5)
    manhattan = get_arrivals(feed, "B06S", limit=5)

    return queens, manhattan


if __name__ == "__main__":
    main()