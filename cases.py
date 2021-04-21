import urllib
import requests
from lxml import html

def updateData():
    url = "https://services8.arcgis.com/K8jt9QACjKo097DD/ArcGIS/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
    page = requests.get(url)
    data = page.json()
    page = requests.get(url)
    data = page.json()


def getCasesIn(city):
    url = "https://services8.arcgis.com/K8jt9QACjKo097DD/ArcGIS/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
    page = requests.get(url)
    data = page.json()
    return str(data['features'][0]['attributes']['Faelle_E_' + city])


def getValue(value):
    url = "https://services8.arcgis.com/K8jt9QACjKo097DD/ArcGIS/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
    page = requests.get(url)
    data = page.json()
    return str(data['features'][0]['attributes'][value])


def getNewCasesInGermany():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr[17]/td[3]/strong/text()"
    page = requests.get(url)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    res = str(tree.xpath(xpath))
    count = res.replace("[", "")
    count = count.replace("'", "")
    count = count.replace("]", "")
    return count
