from real_estate_tools import sqlUtilities, roi
import sqlite3
import pandas as pd
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        description = """
        Calculate the potential profit for properties in buy table.
        """
    )
    parser.add_argument(
        'zip',
        type = int,
        nargs = 1,
        help = "Zip code to look in for purchases/rentals"
    )
    parser.add_argument(
        '--buy-price',
        type = str,
        nargs = 1,
        help = "Sales price threshold."
    )
    parser.add_argument(
        "--rent-price",
        type = str,
        nargs = 1,
        help = "Rent threshold."
    )
    parser.add_argument(
        '--beds',
        type = int,
        nargs = 1,
        help = "Number of beds."
    )
    parser.add_argument(
        '--baths',
        type = float,
        nargs = 1,
        help = "Number of baths."
    )
    parser.add_argument(
        '--sqft',
        type = float,
        nargs = 1,
        help = "Total square footage."
    )

    args = parser.parse_args()
    query = {}

    for arg in ['zip', "buy_price", 'rent_price', 'beds', 'baths', 'sqft']:
        attribute = getattr(args, arg)
        if attribute:
            query[arg] = attribute[0]

    db = sqlUtilities.getDB()
    cur = db.cursor()
    result = roi.calcROI(cur, query)
    print(result)
    sqlUtilities.closeDB(db)