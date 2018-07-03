'''
@Desc
    爬取gatherproxy网站的代理IP和端口信息
@Author yangxi
@date 2018-6-18
'''

import requests
from bs4 import BeautifulSoup
import json
from random import choice
import time

from CommenModel.HeaderModel import HeaderModel
from redis_client import ProxyRedis


class GatherproxyModel(object):

    @classmethod
    def getProxyList(cls):
        '''
        爬取页面的代理IP信息
        :return: 单个以字典形式存储IP信息的list
        '''
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        search_url = 'http://www.gatherproxy.com/zh/'




        try:
            html = get_html_from_proxy(search_url, headers)
        except Exception as e:
            print(e)
            try:
                time.sleep(0.5)
                html = requests.get(search_url, headers=headers).content.decode('utf-8')
            #如果通过服务器本地IP爬网站异常，则调用本方法再次爬取
            except:
                time.sleep(1)
                GatherproxyModel.getProxyList()

        #处理html
        if isinstance(html, 'bytes'):
            html = html.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser').find_all('script')
        proxy_dict = []
        for item in soup:
            if "PROXY_IP" in str(item):
                try:
                    dict_right = str(item).split('(')[1]
                    dict_light = str(dict_right).split(")")[0]
                    dict_info = json.loads(dict_light)
                    proxies_ip = dict_info['PROXY_IP']
                    proxies_port = str(int('{}'.format(dict_info['PROXY_PORT']), 16))
                    proxies_server_location = dict_info['PROXY_COUNTRY']
                    proxies_type = dict_info['PROXY_TYPE']
                    # 连接数
                    proxies_cen = dict_info['PROXY_UPTIMELD']
                    # 延迟
                    proxies_cen_fast = dict_info['PROXY_TIME']
                    proxies_ip_port = '{}:{}'.format(proxies_ip, proxies_port)
                except IndexError:
                    pass
                else:
                    proxy_dict.append({
                        'proxies_ip': proxies_ip,
                        'proxies_port': proxies_port,
                        'proxies_server_location': proxies_server_location,
                        'proxies_type': proxies_type,
                        'proxies_cen': proxies_cen,
                        'proxies_cen_fast': proxies_cen_fast,
                    })
            else:
                pass
        return proxy_dict

def get_html_from_proxy(search_url, headers):
    '''
    通过redis中爬取代理IP请求对应的url
    :param search_url:
    :param headers:
    :return:
    '''
    redis_proxy_dict = ProxyRedis.get_proxy()
    get_proxy = choice(redis_proxy_dict['proxy_data'])['request_get_proxy']
    try:
        html = requests.get(search_url, headers=headers, proxies=get_proxy, timeout=5).content.decode('utf-8')
        return html
    except Exception as e:
        raise e