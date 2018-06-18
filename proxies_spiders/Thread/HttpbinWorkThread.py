import requests
from bs4 import BeautifulSoup
import time
import json

from CommenModel.HeaderModel import HeaderModel
from CommenModel.TaskQueue import TaskQueue

class HttpbinWorkThread(object):
    IS_EMPTY = False

    def __init__(self, queue):
        self.queue = queue


    def processProxy(self, proxy):
        '''
        将代理的字典信息转换成代理IP格式
        :param proxy:
        :return:
        '''
        proxy_ip_port = '{}:{}'.format(proxy['proxies_ip'], proxy['proxies_port'])
        proxy_ip_port_dict = {}
        proxy_ip_port_dict['http'] = 'http://{}'.format(proxy_ip_port)
        proxy_ip_port_dict['https'] = 'https://{}'.format(proxy_ip_port)
        return proxy_ip_port_dict

    def rum(self):
        while self.IS_EMPTY:
            if self.queue.empty():
                self.IS_EMPTY = True
                self.queue.task_done()
                break

            proxy = self.queue.get()
            proxy = self.processProxy(proxy)
            try:
                html = requests.get('https://httpbin.org/ip', headers=HeaderModel.getHeaders(), proxies=proxy, timeout=5)
                if html.status_code != '200':
                    self.queue.put(proxy, 3)
                    time.sleep(10)

                else:
                    soup = BeautifulSoup(html.content, 'html.parser').find('pre').text
                    soup_dic = json.loads(soup)
                    if soup_dic['origin'] in proxy:
                        TaskQueue.putVerificationQueue(proxy)
                    else:
                        pass

            except Exception as e:
                print(e)