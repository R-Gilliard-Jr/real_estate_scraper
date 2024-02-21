from real_estate_tools import realtorClasses, sqlUtilities
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description = "Scrape a real estate website.")
    parser.add_argument(
        'url',
        metavar = 'url',
        type = str,
        nargs = 1,
        help = 'A url to be scraped.'
    )
    args = parser.parse_args()

    dirname = os.path.dirname(__file__)
    json_path = os.path.join(dirname, "credentials.json")

    try:
        credentials = open(json_path)
    except:
        api_key = input("Please enter your google maps API key:")
        credentials = { "google_maps_api_key" : api_key }
        credentials = json.dumps(credentials)
        with open(json_path, 'w') as f:
            f.write(credentials)

    credentials = json.load(credentials)

    rdc = realtorClasses.rdcParser(
        args.url[0],
        credentials
    )

    rdc.getHTML()
    rdc.getPages()
    rdc.getData()
    rdc.cleanData()

    db = sqlUtilities.getDB()
    cur = db.cursor()
    sqlUtilities.insertData(rdc.data, cur, db, rdc.kind)
    sqlUtilities.closeDB(db)