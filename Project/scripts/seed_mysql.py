"""Idempotently load the deterministic 1,000-listing demo data into MySQL."""

from __future__ import annotations

import os
import time

import pymysql

from seed_china_houses import listing_rows


COLUMNS = (
    "user_id", "title", "rent_type", "floor", "all_floor", "house_type", "rooms",
    "position", "area", "price", "intro", "devices", "head_image", "images", "city_id",
    "city_name", "region_id", "region_name", "community_name", "detail_address", "longitude", "latitude",
)
PLACEHOLDERS = ", ".join(["%s"] * len(COLUMNS))
INSERT_SQL = f"INSERT INTO house ({', '.join(COLUMNS)}) VALUES ({PLACEHOLDERS})"


def connect() -> pymysql.Connection:
    for attempt in range(30):
        try:
            return pymysql.connect(
                host=os.environ.get("DB_HOST", "mysql"),
                port=int(os.environ.get("DB_PORT", "3306")),
                user=os.environ.get("DB_USER", "rental"),
                password=os.environ.get("DB_PASSWORD", "rental"),
                database=os.environ.get("DB_NAME", "rental"),
                charset="utf8mb4",
                autocommit=False,
            )
        except pymysql.MySQLError:
            if attempt == 29:
                raise
            time.sleep(2)
    raise RuntimeError("unreachable")


def main() -> None:
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM house")
        if cursor.fetchone()[0] > 0:
            print("House seed skipped: the table already contains data.")
            return
        cursor.executemany(INSERT_SQL, listing_rows())
        connection.commit()
        print("Loaded 1000 deterministic demo rental listings.")


if __name__ == "__main__":
    main()
