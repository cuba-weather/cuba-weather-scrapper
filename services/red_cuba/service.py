# -*- coding: utf-8 -*-
from json import loads
from time import sleep
from urllib.parse import quote
from urllib.request import urlopen

from cubaweatherscrapper import CubaweatherScrapper
from .locations import locations

__service_name__ = 'red_cuba'
__service_version__ = '0.1'

class Red_Cuba(CubaweatherScrapper):

    # service info
    __service_name__ = __service_name__
    __service_version__ = __service_version__

    def __init__(self):

        # init framework parent class
        CubaweatherScrapper.__init__(self)

    def run(self):

        URL = 'https://www.redcuba.cu/api/weather_get_summary/{location}'

        locations_data = []

        for location in locations:
            escaped_location = quote(location)
            url = URL.format(location=escaped_location)
            response = urlopen(url)
            content = response.read()
            if type(content) == bytes:
                content = content.decode()
            data = loads(content)['data']

            locations_data.append(data)
            sleep(1)

        for data in locations_data:
            print(data)

        # call something like:
        # self.send_data(locations_data)
