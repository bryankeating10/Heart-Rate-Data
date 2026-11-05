import numpy as np
import pandas as pd
from scipy import integrate

df = pd.read_csv("garmin_heart_rate.csv")

# Filter for all days from July 1, 2026 onwards
df_filtered = df[df["calendar_date"] >= "2026-07-01"].copy()

# Ensure rows are sorted chronologically
df_filtered = df_filtered.sort_values(["calendar_date", "timestamp_ms"])

print("--- Daily Total Heartbeats ---")

# Group by each calendar date and compute AUC
for current_date, group in df_filtered.groupby("calendar_date", sort=True):
    # Integration requires at least 2 points
    if len(group) < 2:
        print(f"{current_date}: Not enough data points ({len(group)} readings)")
        continue

    # Elapsed minutes relative to the first reading of that day
    elapsed_minutes = (
        (group["timestamp_ms"] - group["timestamp_ms"].min()) / (1000 * 60)
    ).to_numpy()
    hr_values = group["heart_rate_bpm"].to_numpy()

    # Area = (Beats / Minute) * Minutes = Total Heartbeats
    total_heartbeats = integrate.trapezoid(hr_values, x=elapsed_minutes)

    print(
        f"{current_date}: {total_heartbeats:,.0f} beats ({len(group):,} readings)"
    )

records = []
for current_date, group in df_filtered.groupby("calendar_date", sort=True):
    if len(group) >= 2:
        elapsed = (
                (group["timestamp_ms"] - group["timestamp_ms"].min()) / (1000 * 60)
        ).to_numpy()
        hb = integrate.trapezoid(group["heart_rate_bpm"].to_numpy(), x=elapsed)
        records.append(
            {
                "calendar_date": current_date,
                "total_heartbeats": round(hb),
                "readings_count": len(group),
                "avg_bpm": round(group["heart_rate_bpm"].mean(), 1),
            }
        )

summary_df = pd.DataFrame(records)
summary_df.to_csv("daily_heartbeat_summary.csv", index=False)