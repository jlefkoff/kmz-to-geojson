# Copyright Jonah Lefkoff

import xml.etree.ElementTree as ET
import re
import os
import argparse
import zipfile
from geopy.distance import distance
import json


# arg parser
parser = argparse.ArgumentParser(
    description='Converts KMZ radar video maps to GeoJSON.')
parser.add_argument('kmz_path', metavar='kmz_path', type=str,
                    help='The path to a folder of KMZ files to be converted.')
parser.add_argument('json_out', metavar='json_out', type=str,
                    help='The path to output the GeoJSON files.')
parser.add_argument('-r', '--radius',
                    help='The maximum radius of the map in nautical miles. Defaults to 100.', type=int, required=False)
args = parser.parse_args()

# takes a file path to a KMZ file and converts it to a kml to pass to the kml_to_geojson function
def kmz_to_kml(fname):
    zf = zipfile.ZipFile(fname,'r')
    for fn in zf.namelist():
        if fn.endswith('.kml'):
            content = zf.read(fn)
            if args.radius:
              parse_kml_to_geojson(content, fname, args.radius)
            else:
              parse_kml_to_geojson(content, fname)
        else:
            print("no kml file")

# takes a kml file and converts it to a GeoJSON file and writes it to the json_out path

def parse_kml_to_geojson(kml, fname, max_radius=100):
    root = ET.fromstring(kml)

    features = []

    look_at_coordinates = (
        float(root.find('.//{http://earth.google.com/kml/2.0}LookAt/{http://earth.google.com/kml/2.0}longitude').text),
        float(root.find('.//{http://earth.google.com/kml/2.0}LookAt/{http://earth.google.com/kml/2.0}latitude').text)
    )

    for line_string in root.findall('.//{http://earth.google.com/kml/2.0}LineString'):
            coordinates = line_string.find('{http://earth.google.com/kml/2.0}coordinates').text.strip().split()
            
            coordinates_list = []
            for coord in coordinates:
                lon, lat, _ = coord.split(',')
                coordinates_list.append([float(lon), float(lat)])

            # Calculate distance between each point in LineString and LookAt coordinates, needs to be lat long not long lat
            distances = []
            for coord in coordinates_list:
                distances.append(distance([coord[1],coord[0]], [look_at_coordinates[1],look_at_coordinates[0]]).nautical)

            # Filter LineStrings based on the maximum radius
            if max(distances) <= max_radius: 
              feature = {
                  "type": "Feature",
                  "properties": {
                    "color": "#ffffff",
                    "style": "solid",
                    "thickness": "1",
                  },
                  "geometry": {
                      "type": "LineString",
                      "coordinates": coordinates_list
                  }
              }
              features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # get the map name from the file name
    map_name = re.search(r'([a-zA-Z0-9]+)\.kmz', fname).group(1)
    # create the output file named after the input file
    with open(f"{args.json_out}/{map_name}.geojson", "w+") as output_file:
      # write to the file
      json.dump(geojson_data, output_file, indent=2)


# loop through each file in the kmz_path and run the kmz_to_kml function on it
for fname in os.listdir(args.kmz_path):
    kmz_to_kml(f"{args.kmz_path}/{fname}")
