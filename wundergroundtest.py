def clean(str):
    return re.search('-?[0-9]+[.]?[0-9]+',str).group(0)


from wetter24grabber.api.queryapi import WetterQueryApi
api = WetterQueryApi("12099", "16156188")
response = api.call()

re.search('-?[0-9]+[.][0-9]+',response.temp).group(0)