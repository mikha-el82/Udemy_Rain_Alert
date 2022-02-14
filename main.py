import requests
import os
from twilio.rest import Client

# Open Weather Map
api_key = os.environ.get("OWM_API_KEY")
# # Genova
# MY_LAT = 44.407059  # latitude
# MY_LONG = 8.933990  # longitude
# Prague
MY_LAT = 50.075539  # latitude
MY_LONG = 14.437800  # longitude
OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily,alerts",
    "appid": api_key,
}

response = requests.get(OWM_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

# Twilio
account_sid = "AC9cb771b79c76d1804aade1524829bdd4"
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

will_rain = False
for i in range(0, 11):
    weather_id = weather_data["hourly"][i]["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True

if will_rain:
    print("Bring an umbrella. Message sent.")

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Bring an umbrella. It's going to rain today.",
        from_="+18456405249",
        to="+420728403591"
    )
    print(message.status)
else:
    print("No need for an umbrella. No message was sent.")
