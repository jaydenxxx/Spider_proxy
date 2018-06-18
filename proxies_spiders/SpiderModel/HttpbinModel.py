import requests
from bs4 import BeautifulSoup

from CommenModel.HeaderModel import HeaderModel
from CommenModel.TaskQueue import TaskQueue

class HttpbinModel(object):
    def __init__(self, proxy):
        self.proxy = proxy


    def CheckEffective(self):
        html = requests.get('https://httpbin.org/ip', headers=HeaderModel.getHeaders(), proxies=self.proxy, timeout=5)
        if  html.status_code != '200':
            pass

