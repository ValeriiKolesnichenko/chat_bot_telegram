"""The weather telegram-bot"""
import json
import time
from typing import Dict, Any
import requests

import const


def answer_user_bot(data: Dict[str, Any]) -> requests.Response:
    """Answer from bot"""
    data = {
        'chat_id': const.MY_ID,
        'text': data
    }
    url = const.URL.format(TOKEN=const.TOKEN, method=const.SEND_METH)
    response = requests.post(url, data=data)
    return response


def parse_weather_data(data: Dict[str, Any]) -> str:
    """Parsing got data"""
    weather_state = data['weather'][0]['main']
    wind_speed = data['wind']['speed']
    temp = data['main']['temp'] - 273.15
    city = data['name']
    msg = (f'The weather in {city}: temperature is {temp.__round__()}, '
           f'wind speed is {wind_speed} m/s, state is {weather_state}')
    return msg


def get_weather(location: str) -> str:
    """Getting weather"""
    url = const.WEATHER_URL.format(CITY=location, WEATHER_TOKEN=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data: Dict[str, Any]) -> str:
    """Getting message from user"""
    return data['message']['text']


def save_update_id(update: Dict[str, Any]) -> bool:
    """Saving the update_id"""
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
        const.UPDATE_ID = update['update_id']
    return True


def main() -> None:
    """Main function"""
    try:
        while True:
            url = const.URL.format(TOKEN=const.TOKEN, method=const.UPDATE_METH)
            content = requests.get(url).text
            data = json.loads(content)
            result = data['result'][::-1]
            needed_part = None

            for res in result:
                if res['message']['chat']['id'] == const.MY_ID:
                    needed_part = res
                    break

            if const.UPDATE_ID != needed_part['update_id']:
                message = get_message(needed_part)
                msg = get_weather(message)
                answer_user_bot(msg)
                save_update_id(needed_part)

            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
