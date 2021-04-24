import urllib
import requests
from lxml import html
import re

fallURL = "https://services8.arcgis.com/K8jt9QACjKo097DD/ArcGIS/rest/services/Corona_Dashboard_Einz/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
rkiURL = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"


def getCasesIn(city):
    url = fallURL
    page = requests.get(url)
    data = page.json()
    return str(data['features'][0]['attributes']['Faelle_E_' + city])


def getValue(value):
    url = fallURL
    page = requests.get(url)
    data = page.json()
    return str(data['features'][0]['attributes'][value])


def getXPath(url, xpath):
    page = requests.get(url)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    res = str(tree.xpath(xpath))
    count = res.replace("[", "")
    count = count.replace("'", "")
    count = count.replace("]", "")
    return count


def getSevenDayIncidence():
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr[17]/td[5]/strong/text()"
    return str(getXPath(rkiURL, xpath).replace(".", ""))


def getNewCasesInGermany():
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr[17]/td[3]/strong/text()"
    return str(getXPath(rkiURL, xpath).replace(".", ""))


def getAllCasesInGermany():
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr[17]/td[2]/strong/text()"
    return str(getXPath(rkiURL, xpath).replace(".", ""))


def getDeathsInGermany():
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr[17]/td[6]/strong/text()"
    return str(getXPath(rkiURL, xpath).replace(".", ""))


def getDateRKI():
    xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/p[1]/text()"
    return str(re.sub('[^0-9.]','',getXPath(rkiURL,xpath)[6:25]))