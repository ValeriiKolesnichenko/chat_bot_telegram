"""This bot will give a weather about the city which we will point out at """
import requests
import json
import time
import const


def answer_user_bot(data):
    """This function will make a weather report for user"""
    data = {
        'chat_id': const.MY_ID,
        'text': data
    }
    url = const.URL.format(TOKEN=const.TOKEN, method=const.SEND_METH)
    # Getting a response
    response = requests.post(url, data=data)
    return response


def parse_weather_data(data):
    """This function will parse the data we've got from weather website"""
    weather_state = data['weather'][0]['main']
    wind_speed = data['wind']['speed']
    temp = data['main']['temp'] - 273.15
    city = data['name']
    # Making a message for user
    msg = (f'The weather in {city}: temperature is {temp.__round__()}, '
           f'wind speed is {wind_speed} m/s, state is {weather_state}')
    return msg


def get_weather(location):
    """This function will return parsed weather data for user"""
    url = const.WEATHER_URL.format(CITY=location, WEATHER_TOKEN=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    # Deserialization of data
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data):
    """This function returns user message"""
    return data['message']['text']


def save_update_id(update):
    """This function saves update id in special file 'update_id'"""
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
        const.UPDATE_ID = update['update_id']
    return True


def main():
    """Main function - the body of the program"""
    try:
        while True:
            # Forming the URL for getting updates from Telegram
            url = const.URL.format(TOKEN=const.TOKEN, method=const.UPDATE_METH)
            content = requests.get(url).text

            # Parsing the JSON content
            data = json.loads(content)
            result = data['result'][::-1]
            needed_part = None

            for res in result:
                if res['message']['chat']['id'] == const.MY_ID:
                    needed_part = res
                    break

            # Checking if the update_id is different from the last saved one
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
