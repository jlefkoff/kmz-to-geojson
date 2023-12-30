# FAA KMZ to GeoJSON

This tool is used to convert FAA provided radar video maps that come as a KMZ into GeoJSON files for import to the [vNAS system](https://vnas.vatsim.net/).

# Usage

First install the required library (geopy) by running `pip install -r requirements.txt` in the root of this repository.

Then run `python3 convert.py` and provide the arguments `kmz_path json_out` where `kmz_path` is the path to the directory of KMZ files and `json_out` is the path to the folder where you would like the output files to be placed.

# Notes

This tool by default removes any linestrings beyond 100nm from the center of the map. This is because the KMZ RVMs contain a circular border and map text which is unecessary in CRC. The radius can be optionally changed by passing the `--radius` argument to the script.

# License

This project is licensed under [GPL 3.0](https://github.com/jlefkoff/kmz-to-geojson/blob/main/LICENSE)
