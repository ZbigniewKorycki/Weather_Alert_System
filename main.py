import requests
from twilio.rest import Client
import config

account_sid = config.account_sid
auth_token = config.auth_token
API_KEY = config.API_KEY

client = Client(account_sid, auth_token)

MY_LATITUDE = config.MY_LATITUDE
MY_LONGITUDE = config.MY_LATITUDE


parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": API_KEY,
}

connection = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast", params=parameters
)
connection.raise_for_status()
weather_data_12h = connection.json()["list"][:12]


will_rain = False

for weather_id in weather_data_12h:
    condition_code = weather_id["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today.",
        from_=config.phone_number_sender,
        to=config.phone_number_recipient,
    )
    print(message.status)
