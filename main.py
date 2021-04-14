from decouple import config
import requests
import json

API_KEY = config('API_KEY')
URL = config('URL')

def get_weather_info(city):
    weather_url = f'{URL}weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url=weather_url)
    if response.status_code == 404:
        print("City not found")
        return
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f'Current Weather at {city.capitalize()}: \n' \
              f'{data["weather"][0]["description"].capitalize()} \n' \
              f'Current Temperature: {data["main"]["temp"]}°C \n'\
              f'Temperature feels like: {data["main"]["feels_like"]}°C \n'\
              f'Max Temperature: {data["main"]["temp_max"]}°C \n' \
              f'Min Temperature: {data["main"]["temp_min"]}°C \n' \
              f'Humidity: {data["main"]["humidity"]}% \n' \
              f'Pressure: {data["main"]["pressure"]}hPa \n'
              f'Visibility: {data["visibility"]}mts. \n'\
              f'Wind: Speed{data["wind"]["speed"]}Km/h, Direction{data["wind"]["deg"]}°')
        return
    if response.status_code == 429:
        print("Minute request limit reached...")
        return
    if response.status_code == 401:
        print("Please check you API and subscription status")
        return


if __name__ == '__main__':
    city = input("Please input city you wish to get weather information: ")
    get_weather_info(city)

