import redis
import json
import time

from CommenModel.TaskQueue import TaskQueue

def get_redis_pool():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='199redis-pwd', db=0)
    r = redis.StrictRedis(connection_pool=pool)
    return r

class ProxyRedis():
    @staticmethod
    def start():
        print("开始写入redis！")
        r = get_redis_pool()
        '''
        将每个代理IP的dict格式转换成json格式
        :return:
        '''
        proxy_list = []
        verificationQueue = TaskQueue.getVerificationQueue()

        while not TaskQueue.isVerificationQueueEmpty():
            proxy_list.append(verificationQueue.get())

        add_time = time.strftime("%Y-%m-%d %H:%M:%S")
        result = json.dumps({
            'proxy_data': proxy_list,
            'add_time': add_time,
        })

        r.set('proxies', result)
        print("执行完成！")

    @staticmethod
    def get_proxy():
        r = get_redis_pool()
        proxy_dict = json.loads(r.get("proxies"))
        return proxy_dict