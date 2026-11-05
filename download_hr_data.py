import csv
import json
import os
import sys
import time
from datetime import date, timedelta
from garmin_personal_api import (
    GarminPersonalApiClient,
    HttpError,
    PersonalApiAuthenticator,
    resolve_api_key,
)

def get_heart_rate_with_retry(client, date_string, max_retries=5):
    for attempt in range(max_retries + 1):
        try:
            return client.get_daily_heart_rate(date_string)
        except HttpError as e:
            if e.status_code != 429:
                raise

            try:
                response = json.loads(e.response_text)
                wait_time = int(response.get("retryInSeconds", 60))
            except (ValueError, TypeError):
                wait_time = 60

            wait_time += 2  # Small safety buffer

            print(
                f"Rate limited on {date_string}. "
                f"Waiting {wait_time} seconds. "
                f"Retry {attempt + 1}/{max_retries}"
            )

            if attempt == max_retries:
                raise

            time.sleep(wait_time)


print("Python interpreter:", sys.executable)
print("Garmin API key exists:", bool(os.getenv("GARMIN_PERSONAL_API_KEY")))

# Date range: July 1, 2026 through the current date
start_date = date(2026, 7, 1)
end_date = date.today()

output_file = "garmin_heart_rate.csv"

with PersonalApiAuthenticator() as auth:
    token = auth.obtain_token(resolve_api_key())

    with GarminPersonalApiClient(token.access_token) as client:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["calendar_date", "timestamp_ms", "heart_rate_bpm"])

            current_date = start_date
            total_readings = 0

            while current_date <= end_date:
                date_string = current_date.isoformat()

                try:
                    # Using retry helper function to handle 429 rate limits
                    data = get_heart_rate_with_retry(client, date_string)

                    readings = data.get("heartRateValues") or []

                    for timestamp, heart_rate in readings:
                        if heart_rate is not None:
                            writer.writerow([date_string, timestamp, heart_rate])
                            total_readings += 1

                    print(f"{date_string}: {len(readings)} readings")

                except Exception as e:
                    print(f"ERROR on {date_string}: {e}")

                f.flush()

                current_date += timedelta(days=1)
                time.sleep(0.25)

print(f"\nDownload complete: {total_readings} readings")
print(f"Saved to {output_file}")