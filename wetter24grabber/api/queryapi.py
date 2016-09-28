import requests
from bs4 import BeautifulSoup
from wetter24grabber import Response
import re

class WetterQueryApi(object):
    def __init__(self, plz, region):
        self.plz = plz
        self.region = region

    def call(self):
        def clean(str):
            return re.search('-?\d+\.?\d*',str).group(0)

        response = requests.get("http://www.wetter24.de/vorhersage/deutschland/"+ self.plz + "/" + self.region+"/")
        #response = requests.get("http://www.wetter24.de/vorhersage/deutschland/"+ "12099" + "/" + "16156188" + "/")
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            temp = soup.find("div", {"class":"mg_box_simple overview currentWeather"}).find("span", {"class":"temp_val"}).text
            wind = soup.find("div", {"class":"mg_box_simple overview currentWeather"}).find("span", {"class":"wval"}).text
            sun  = soup.find("div", {"class":"forecast_teaser"}).find("td", {"class":"sunamount"}).text
            rain  = soup.find("div", {"class":"forecast_teaser"}).find("td", {"class":"rainamount"}).text
            return Response(
                False, 
                self.plz, 
                self.region, 
                clean(temp), 
                clean(wind), 
                clean(sun),
                clean(rain)
            )
        else: 
            return Response(False, self.plz, self.region, None, None, None, None) 






