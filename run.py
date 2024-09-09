import csv
import io

import h3
import requests

res = requests.get("https://www.chattadata.org/api/views/nvdi-c4tt/rows.csv")

with io.StringIO(res.text) as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    rows = list(reader)

# add cell_id to rows
for row in rows:
    if row['Latitude'] and row['Longitude']:
        latitude = float(row['Latitude'])
        longitude = float(row['Longitude'])
        resolution = 5
        row['h3_cell_id'] = h3.latlng_to_cell(latitude, longitude, 3)

with open("data.csv", "w", newline="") as f:
    new_fieldnames = columns + ['h3_cell_id']
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(rows)
