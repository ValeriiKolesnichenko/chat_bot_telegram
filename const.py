

TOKEN = '6918937155:AAHjwS_-A6Sa1Y0HILEJFHW0yXjIjT5s9D4'

URL = 'https://api.telegram.org/bot{TOKEN}/{method}'

UPDATE_METH = 'getUpdates'
SEND_METH = 'sendMessage'

MY_ID = 624736023

UPDATE_ID_FILE_PATH = 'update_id'

with open(UPDATE_ID_FILE_PATH) as file:
    data = file.readline()
    if data:
        data = int(data)
    UPDATE_ID = data

WEATHER_TOKEN = '20403524aa6ebf95646fabdc9287c149'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_TOKEN}'



