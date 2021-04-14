from decouple import config
import requests
import json

API_KEY = config('API_KEY')
URL = config('URL')


def get_weather_info(city_name):
    weather_url = f'{URL}weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url=weather_url)
    if response.status_code == 404:
        print("City not found")
        return
    if response.status_code == 200:
        return json.loads(response.content)
    if response.status_code == 429:
        print("Minute request limit reached...")
        return
    if response.status_code == 401:
        print("Please check you API and subscription status")
        return


def get_wind_cardinal_direction(data):
    cardinal = ""
    if 0 <= data["wind"]["deg"] < 33.75:
        cardinal = "N"
    elif 33.75 <= data["wind"]["deg"] < 78.75:
        cardinal = "NE"
    elif 78.75 <= data["wind"]["deg"] < 123.75:
        cardinal = "E"
    elif 123.75 <= data["wind"]["deg"] < 213.75:
        cardinal = "SE"
    elif 213.75 <= data["wind"]["deg"] < 258.75:
        cardinal = "SW"
    elif 258.75 <= data["wind"]["deg"] < 303.75:
        cardinal = "W"
    elif 303.75 <= data["wind"]["deg"] < 348.75:
        cardinal = "NW"
    elif 348.75 <= data["wind"]["deg"] < 360:
        cardinal = "N"
    return cardinal


def print_weather_info(city_name):
    data = get_weather_info(city_name)
    if data:
        cardinal = get_wind_cardinal_direction(data)
        print(f'Current Weather at {city_name.capitalize()}: \n' \
              f'{data["weather"][0]["description"].capitalize()} \n' \
              f'Current Temperature: {data["main"]["temp"]}°C \n' \
              f'Temperature feels like: {data["main"]["feels_like"]}°C \n' \
              f'Max Temperature: {data["main"]["temp_max"]}°C \n' \
              f'Min Temperature: {data["main"]["temp_min"]}°C \n' \
              f'Humidity: {data["main"]["humidity"]}% \n' \
              f'Pressure: {data["main"]["pressure"]}hPa \n' \
              f'Visibility: {data["visibility"]/1000:.2f}Km. \n' \
              f'Wind: \n' \
              f'\tSpeed: {data["wind"]["speed"]*1.60934:.2f}Km/h \n'
              f'\tDirection: {data["wind"]["deg"]}° {cardinal}')
    else:
        return


if __name__ == '__main__':
    city = input("Please input city you wish to get weather information: ")
    print_weather_info(city)

