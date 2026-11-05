
import json

from garmin_personal_api import (
    GarminPersonalApiClient,
    PersonalApiAuthenticator,
    resolve_api_key,
)

test_date = "2026-10-04"

# Authenticate with Garmin
with PersonalApiAuthenticator() as auth:
    token = auth.obtain_token(resolve_api_key())

    # Create authenticated API client
    with GarminPersonalApiClient(token.access_token) as client:

        # Request daily heart rate
        data = client.get_daily_heart_rate(test_date)

        print("\n--- RAW GARMIN RESPONSE ---")
        print(json.dumps(data, indent=4))

        print("\n--- RESPONSE TYPE ---")
        print(type(data))

        if isinstance(data, dict):
            print("\n--- RESPONSE KEYS ---")
            print(data.keys())

            print("\n--- HEART RATE VALUES ---")
            print(data.get("heartRateValues"))
