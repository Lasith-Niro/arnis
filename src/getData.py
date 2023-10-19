import os
import requests
from random import choice


def getData(bbox, debug):
    print("Fetching data...")
    bbox = bbox.split(",")
    # convert bbox to float
    bbox = [float(i) for i in bbox]
    server = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json][bbox:{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}];
        ( 
        way["highway"];
        way["building"];
        way["water"];
        way["landuse"];
        relation["water"];
        relation["landuse"];
        relation["highway"];
        relation["building"];
        );
        (._;>;);
        out;
        """
    if debug:
        print(overpass_query)
    try:
        data = requests.get(server, params={"data": overpass_query}).json()

        if len(data["elements"]) == 0:
            print("Error! No data available")
            os._exit(1)
    except Exception as e:
        if "The server is probably too busy to handle your request." in str(e):
            print("Error! OSM server overloaded")
        elif "Dispatcher_Client::request_read_and_idx::rate_limited" in str(e):
            print("Error! IP rate limited")
        else:
            print(f"Error! {e}")
        os._exit(1)

    # if debug:
    with open("arnis-debug-raw_data.json", "w", encoding="utf-8") as f:
        f.write(str(data))
    return data