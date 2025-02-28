
import pandas as pd
import xml.etree.ElementTree as ET
import xarray as xr

# Define file path
xml_path = "data/sampleRaceResults/del20230708tch.xml"

# Parse XML
tree = ET.parse(xml_path)
root = tree.getroot()

# Extract track and race date information
track_info = root.find("TRACK")
track_id = track_info.findtext("CODE", "Unknown")
track_name = track_info.findtext("NAME", "Unknown")
race_date = root.get("RACE_DATE", "Unknown")

# Collect race data
race_entries = []

for race in root.findall("RACE"):
    race_number = int(race.get("NUMBER", -1))
    purse = float(race.findtext("PURSE", 0.0))
    distance = int(race.findtext("DISTANCE", 0))
    track_condition = race.findtext("TRK_COND", "Unknown")

    for entry in race.findall("ENTRY"):
        horse_name = entry.findtext("NAME", "Unknown")
        
        jockey_elem = entry.find("JOCKEY")
        jockey_name = " ".join(filter(None, [
            jockey_elem.findtext("FIRST_NAME", ""),
            jockey_elem.findtext("MIDDLE_NAME", ""),
            jockey_elem.findtext("LAST_NAME", ""),
        ])).strip() if jockey_elem is not None else "Unknown"

        trainer_elem = entry.find("TRAINER")
        trainer_name = " ".join(filter(None, [
            trainer_elem.findtext("FIRST_NAME", ""),
            trainer_elem.findtext("MIDDLE_NAME", ""),
            trainer_elem.findtext("LAST_NAME", ""),
        ])).strip() if trainer_elem is not None else "Unknown"

        finishing_position = int(entry.findtext("OFFICIAL_FIN", -1))
        odds = float(entry.findtext("DOLLAR_ODDS", 0.0))

        # Append race data
        race_entries.append({
            "trackID": track_id, "trackName": track_name, "raceDate": race_date,
            "raceNumber": race_number, "horse": horse_name, "jockey": jockey_name,
            "trainer": trainer_name, "finishingPosition": finishing_position,
            "odds": odds, "purse": purse, "distance": distance, 
            "trackCondition": track_condition
        })

# Convert to DataFrame
df = pd.DataFrame(race_entries)

# Convert to xarray Dataset
ds = df.set_index(["trackID", "trackName", "raceDate", "raceNumber", "horse"]).to_xarray()

# Save as NetCDF
output_path = "students/wagner_riley/race_results.nc"
ds.to_netcdf(output_path)

print(ds)
