import json
import csv
from pathlib import Path

input_path = Path("dataNetlogo/In_Out_15min.geojson")
output_path = Path("dataNetlogo/flow_counts.csv")

with input_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for feature in data["features"]:
    props = feature["properties"]

    name = props["name"]
    zone_id = name.split("_")[-1]

    direction = props["zoneType"]  # inflow / outflow
    modality = props["modality"]   # bike / pedestrian / vehicle

    if modality == "vehicle":
        mode = "car"
    else:
        mode = modality

    for item in props["flowProfile"]:
        rows.append({
            "slot": item["slot"],
            "time_label": item["timeLabel"],
            "zone_id": zone_id,
            "mode": mode,
            "direction": direction,
            "value": item["value"]
        })

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["slot", "time_label", "zone_id", "mode", "direction", "value"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} rows to {output_path}")