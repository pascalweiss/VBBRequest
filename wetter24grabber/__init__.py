class Response(object):
    def __init__(self,state, plz, region, temp, wind, sun, rain):
        self.state = state
        self.plz = plz
        self.region = region
        self.temp = temp
        self.sun = sun
        self.wind = wind
        self.rain = rain