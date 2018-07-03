import requests
from bs4 import BeautifulSoup
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

            #包括代理IP信息的dict类型数据
            proxy_dict = self.queue.get()
            #符合get方法的代理IP格式类型
            proxy = self.processProxy(proxy_dict)
            try:
                html = requests.get('https://httpbin.org/ip', headers=HeaderModel.getHeaders(), proxies=proxy)
                #请求httpbin非200
                if html.status_code != 200:
                    print('线程执行结果：无效代理IP')

                #请求httpbin成功
                else:
                    # soup = BeautifulSoup(html.content, 'html.parser').find('pre').text
                    soup_dic = json.loads(html.text)
                    #请求结果的IP和代理IP 相同
                    if soup_dic['origin'] in str(proxy):
                        proxy_item = {
                            'proxy_info': proxy_dict,
                            'request_get_proxy': proxy,
                        }
                        TaskQueue.putVerificationQueue(proxy_item)
                        print('线程执行结果：代理IP{}为有效！,剩余待执行{}'.format(soup_dic, len(self.queue.queue)))
                    # 请求结果的IP和代理IP不 相同
                    else:
                        pass
            #请求异常
            except Exception as e:
                print('线程执行结果：异常{}！,剩余待执行{}'.format(e, len(self.queue.queue)))