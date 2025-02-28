import xml.etree.ElementTree as ET
import xarray as xr
import numpy as np

xml_path = "data/sampleRaceResults/del20230708tch.xml"

# Parse the XML file
tree = ET.parse(xml_path)
root = tree.getroot()

# Extract track details
track_element = root.find("TRACK")
track_id = track_element.findtext("CODE") if track_element is not None else None
track_name = track_element.findtext("NAME") if track_element is not None else None

# Extract race date at the CHART level (applies to all races)
race_date = root.get("RACE_DATE")

# Initialize lists to store race and entry-level data
race_dates = []
race_numbers = []
entries = []
jockeys = []
trainers = []
finishing_positions = []
odds = []
track_conditions = []

# Race-specific lists
unique_race_dates = []
unique_race_numbers = []
purses = []
distances = []

# Iterate through RACE elements
for race in root.findall("RACE"):
    race_number = race.get("NUMBER")  # Extract race number
    purse = race.findtext("PURSE")  # Race purse
    distance = race.findtext("DISTANCE")  # Race distance
    track_condition = race.findtext("TRK_COND")  # Track condition

    # Store race-specific data only once per race
    unique_race_dates.append(race_date)
    unique_race_numbers.append(race_number)
    purses.append(purse if purse else "NA")
    distances.append(distance if distance else "NA")

    for entry in race.findall("ENTRY"):
        horse_name = entry.findtext("NAME")

        # Extract jockey name
        jockey = entry.find("JOCKEY")
        jockey_name = " ".join(filter(None, [
            jockey.findtext("FIRST_NAME") if jockey is not None else None,
            jockey.findtext("MIDDLE_NAME") if jockey is not None else None,
            jockey.findtext("LAST_NAME") if jockey is not None else None,
        ]))

        # Extract trainer name
        trainer = entry.find("TRAINER")
        trainer_name = " ".join(filter(None, [
            trainer.findtext("FIRST_NAME") if trainer is not None else None,
            trainer.findtext("MIDDLE_NAME") if trainer is not None else None,
            trainer.findtext("LAST_NAME") if trainer is not None else None,
        ]))

        # Extract finishing position and odds
        finishing_position = entry.findtext("OFFICIAL_FIN")
        dollar_odds = entry.findtext("DOLLAR_ODDS")

        # Append extracted data (ensuring race attributes are per entry)
        race_dates.append(race_date)
        race_numbers.append(race_number)
        entries.append(horse_name)
        jockeys.append(jockey_name)
        trainers.append(trainer_name)
        finishing_positions.append(finishing_position if finishing_position else "NA")
        odds.append(dollar_odds if dollar_odds else "NA")
        track_conditions.append(track_condition if track_condition else "NA")

# Convert lists to numpy arrays
race_dates = np.array(race_dates, dtype=str)
race_numbers = np.array(race_numbers, dtype=str)
entries = np.array(entries, dtype=str)
jockeys = np.array(jockeys, dtype=str)
trainers = np.array(trainers, dtype=str)
finishing_positions = np.array(finishing_positions, dtype=str)
odds = np.array(odds, dtype=str)
track_conditions = np.array(track_conditions, dtype=str)

# Convert unique race-level data to numpy arrays
unique_race_dates = np.array(unique_race_dates, dtype=str)
unique_race_numbers = np.array(unique_race_numbers, dtype=str)
purses = np.array(purses, dtype=str)
distances = np.array(distances, dtype=str)

# Ensure reshaping is consistent
if len(unique_race_dates) != len(purses):
    raise ValueError(f"Mismatch in race-level dimensions: {len(unique_race_dates)} race dates vs. {len(purses)} purses.")

# Create xarray Dataset
ds = xr.Dataset(
    {
        "finishing_position": (["ENTRY"], finishing_positions),
        "odds": (["ENTRY"], odds),
        "purse": (["RACE_DATE"], purses),
        "distance": (["RACE_DATE"], distances),
        "track_condition": (["ENTRY"], track_conditions),
    },
    coords={
        "TRACK": [track_id],
        "track_name": ("TRACK", [track_name]),
        "RACE_DATE": unique_race_dates,
        "RACE_NUMBER": unique_race_numbers,
        "ENTRY": entries,
        "jockey": ("ENTRY", jockeys),
        "trainer": ("ENTRY", trainers),
    },
)

# Display the dataset
print(ds)
