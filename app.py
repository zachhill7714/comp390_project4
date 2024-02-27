from requests import get
from requests import exceptions
from json import loads
from datetime import datetime

def app():
    print("Hello world")

    api_key = get_api_key()[0]

    user_input = ""
    while user_input == "":
        user_input = input("Enter the zipcode you want to see the weather for: ")

    try:
        location_data = get(f"http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={api_key}&q={user_input}", timeout=5)
    except exceptions.Timeout:
        print("Getting data timed out, please try again")
        return

    if location_data.status_code != 200:
        print("Could not fetch the data, please try again")
        return

    json_location_data = loads(location_data.text)

    location_code = ""
    city = ""
    state = ""
    if json_location_data:
        location_code = json_location_data[0]["ParentCity"]["Key"]
        city = json_location_data[0]["LocalizedName"]
        state = json_location_data[0]["AdministrativeArea"]["LocalizedName"]
        print(f"Your location is: {city}, {state}")

    try:
        current_conditions = get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_code}?apikey={api_key}", timeout=5)
    except exceptions.Timeout:
        print("Getting data timed out, please try again")
        return

    if current_conditions.status_code != 200:
        print("Could not fetch the data, please try again")
        return

    json_current_conditions = loads(current_conditions.text)

    current_conditions_string = ""
    if json_current_conditions:
        weather = json_current_conditions[0]["WeatherText"]
        temperature = json_current_conditions[0]["Temperature"]["Imperial"]["Value"]
        current_conditions_string += f"It is currently {weather} and {temperature} degrees F in {city}, {state}"

    print(current_conditions_string)

    try:
        five_day_forecast = get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}?apikey={api_key}", timeout=5)
    except exceptions.Timeout:
        print("Getting data timed out, please try again")
        return

    if five_day_forecast.status_code != 200:
        print("Could not fetch the data, please try again")
        return

    json_five_day_forecast = loads(five_day_forecast.text)

    if json_five_day_forecast:
        print("The forecast for the next 5 days is as follows: ")

        forecasts = json_five_day_forecast["DailyForecasts"]

        for forecast in forecasts:
            print(f'Forecast for {datetime.fromtimestamp(forecast["EpochDate"]).strftime("%m/%d/%Y")}:')
            print(f'\tMin - {forecast["Temperature"]["Minimum"]["Value"]} degrees F')
            print(f'\tMax - {forecast["Temperature"]["Maximum"]["Value"]} degrees F')
            print(f'\tDay - {forecast["Day"]["IconPhrase"]}')
            print(f'\tNight - {forecast["Night"]["IconPhrase"]}')


def get_api_key():
    file = open("config.txt", "r")

    keys = []
    for line in file.readlines():
        keys.append(line.split("=")[1])

    return keys


if __name__ == "__main__":
    app()
