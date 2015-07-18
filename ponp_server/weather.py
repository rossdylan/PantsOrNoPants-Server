import requests
import urllib
from collections import defaultdict
from pprint import pprint


base_url = 'https://query.yahooapis.com/v1/public/yql?{0}&format=json'
geo_cache = defaultdict(lambda: defaultdict(dict))  # blargh


def query_yql(yql):
    return requests.get(base_url.format(urllib.urlencode({'q': yql}))).json()


def query_location(lat, lng):
    if lat in geo_cache and lng in geo_cache[lng]:
        loc = geo_cache[lat][lng]
    else:
        loc_query = query_yql('SELECT * FROM geo.placefinder WHERE text="{0},{1}" and gflags="R"'.format(lat, lng))
        loc = loc_query['query']['results']['Result']
        geo_cache[lat][lng] = loc
    return loc


def get_weather(lat, lng):
    loc = query_location(lat, lng)
    yql = 'select wind,atmosphere,item from weather.forecast where woeid={0}'
    data = query_yql(yql.format(loc['woeid']))
    weather = {}
    deeper = data['query']['results']['channel']
    weather['wind_speed'] = deeper['wind']['speed']
    weather['humidity'] = deeper['atmosphere']['humidity']
    weather['pressure'] = deeper['atmosphere']['pressure']
    weather['current_temp'] = deeper['item']['condition']['temp']
    weather['high_temp'] = deeper['item']['forecast'][0]['high']
    weather['low_temp'] = deeper['item']['forecast'][0]['low']
    return weather
