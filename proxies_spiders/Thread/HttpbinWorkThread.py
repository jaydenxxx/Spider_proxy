import requests
from bs4 import BeautifulSoup
import time
import json
import threading

from CommenModel.HeaderModel import HeaderModel
from CommenModel.TaskQueue import TaskQueue

class HttpbinWorkThread(threading.Thread):
    IS_EMPTY = False

    def __init__(self, queue):
        threading.Thread.__init__(self)
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

    def run(self):
        while not self.IS_EMPTY:
            if self.queue.empty():
                self.IS_EMPTY = True
                self.queue.task_done()
                break

            proxy = self.queue.get()
            proxy = self.processProxy(proxy)
            try:
                html = requests.get('https://httpbin.org/ip', headers=HeaderModel.getHeaders(), proxies=proxy)
                if html.status_code != 200:
                    print('线程执行结果：请求code非200，重新加入队列')
                    self.queue.put(proxy, 3)
                    time.sleep(10)

                else:
                    # soup = BeautifulSoup(html.content, 'html.parser').find('pre').text
                    soup_dic = json.loads(html.text)
                    if soup_dic['origin'] in str(proxy):
                        TaskQueue.putVerificationQueue(proxy)
                        print('线程执行结果：代理IP{}为有效！,剩余待执行{}'.format(soup_dic, len(self.queue.queue)))
                    else:
                        pass

            except Exception as e:
                print('线程执行结果：异常{}！,剩余待执行{}'.format(e, len(self.queue.queue)))