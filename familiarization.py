# Getting used to the data format and capabilities
import pandas as pd

df = pd.read_csv("garmin_heart_rate.csv")

# Convert milliseconds to datetime (UTC)
df["datetime_utc"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)

# Convert to a specific local timezone (e.g., US Eastern)
df["datetime_local"] = df["datetime_utc"].dt.tz_convert("America/New_York")

print(df.head())
print(df["datetime_local"].head())

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# 1. Load data and filter for the target date
csv_file = "garmin_heart_rate.csv"
target_date = "2026-08-19"

df = pd.read_csv(csv_file)
day_df = df[df["calendar_date"] == target_date].copy()

if day_df.empty:
    raise ValueError(f"No records found for {target_date} in {csv_file}")

# 2. Convert epoch ms to UTC, then convert to local system timezone
# (Change tz_localize / tz_convert if you want a specific timezone, e.g., 'America/New_York')
day_df["datetime"] = (
    pd.to_datetime(day_df["timestamp_ms"], unit="ms", utc=True)
    .dt.tz_convert(None)  # Strips UTC tz info after conversion if using UTC
    # To convert to your local timezone, use:
    # .dt.tz_convert('America/New_York')
)

# 3. Calculate summary metrics
min_hr = day_df["heart_rate_bpm"].min()
max_hr = day_df["heart_rate_bpm"].max()
avg_hr = day_df["heart_rate_bpm"].mean()

# 4. Plot
fig, ax = plt.subplots(figsize=(13, 5), dpi=100)

ax.plot(
    day_df["datetime"],
    day_df["heart_rate_bpm"],
    color="#d93829",
    linewidth=1.2,
    alpha=0.9,
    label="Heart Rate (bpm)",
)

# Optional: fill area below curve
ax.fill_between(
    day_df["datetime"],
    day_df["heart_rate_bpm"],
    min_hr,
    color="#d93829",
    alpha=0.1,
)

# Horizontal reference line for average HR
ax.axhline(
    avg_hr,
    color="#2c3e50",
    linestyle="--",
    linewidth=1,
    alpha=0.7,
    label=f"Avg HR: {avg_hr:.1f} bpm",
)

# Format X-axis to show hours (every 2 hours)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
fig.autofmt_xdate(rotation=0, ha="center")

# Styling
ax.set_title(
    f"Garmin Daily Heart Rate — {target_date} (Min: {min_hr} | Avg: {avg_hr:.1f} | Max: {max_hr})",
    fontsize=13,
    weight="bold",
    pad=12,
)
ax.set_xlabel("Time of Day", fontsize=11, labelpad=8)
ax.set_ylabel("Heart Rate (BPM)", fontsize=11, labelpad=8)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right", frameon=True)
ax.set_ylim(bottom=max(30, min_hr - 10), top=max_hr + 10)

plt.tight_layout()
plt.show()