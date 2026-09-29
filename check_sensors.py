"""
Script to check laboratory equipment calibration status.
Read target settings from a YAML file, look up sensor locations 
in an Excel sheet, process calibration logs from a CSV file, 
and output the out-of-date sensors to a JSON file
"""

import yaml
import pandas as pd
import json


# Read config.yml and get max_days_since_calibration and output_file
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

max_days = config.get("max_days_since_calibration")
output_file = config.get("output_file")


# Read sensors.xlxs
df_sensors = pd.read_excel("sensors.xlsx")

# Read calibrations.csv
df_calibrations = pd.read_csv("calibrations.csv")

# Match each sensor's location/owner with its calibration status
df_joined = pd.merge(df_sensors, df_calibrations, on="sensor_id", how="inner")


# Indentify sensors where days_since_callibrations > max_days_since_calibration
df_overdue = df_joined[df_joined["days_since_calibration"] > max_days]

"""
Export the overdue sensors as a formatted JSON array to the filename
specified in config.yml using json.dump(..., indent=2)
This json file should include sensor_id, lab/owner information as well as
days_since_calibration for the overdue sensors only
"""
overdue_list = df_overdue.to_dict(orient="records")

with open(output_file, "w") as f:
    json.dump(overdue_list, f, indent=2)