from SpiderModel.GatherproxyModel import GatherproxyModel
from CommenModel.TaskQueue import TaskQueue
from Thread.HttpbinWorkThread import HttpbinWorkThread

def startSpider():
    THREAD_NUM = 6

    unverifiedList = GatherproxyModel.getProxyList()

    unverifiedQueue = TaskQueue.getUnverifiedQueue()

    for item in unverifiedList:
        unverifiedQueue.put(item, 3)

    for i in range(THREAD_NUM):
        workThraed = HttpbinWorkThread(unverifiedQueue)
        workThraed.start()

    for proxy_item in TaskQueue.getVerificationQueue():
        print(proxy_item)



if __name__ == '__main__':
    startSpider()