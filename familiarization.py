# Getting used to the data format and capabilities
import pandas as pd

df = pd.read_csv("garmin_heart_rate.csv")

# Convert milliseconds to datetime (UTC)
df["datetime_utc"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)

# Convert to a specific local timezone (e.g., US Eastern)
df["datetime_local"] = df["datetime_utc"].dt.tz_convert("America/New_York")

print(df.head())