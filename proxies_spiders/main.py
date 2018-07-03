from SpiderModel.GatherproxyModel import GatherproxyModel
from CommenModel.TaskQueue import TaskQueue
from Thread.HttpbinWorkThread import HttpbinWorkThread
from redis_client import ProxyRedis

import asyncio
import concurrent.futures as cf

def startSpider():
    THREAD_NUM = 6

    unverifiedList = GatherproxyModel.getProxyList()

    unverifiedQueue = TaskQueue.getUnverifiedQueue()

    for item in unverifiedList:
        unverifiedQueue.put(item, 3)

    for i in range(THREAD_NUM):
        workThraed = HttpbinWorkThread(unverifiedQueue)
        workThraed.start()

    workThraed.join()
    workThraed.clean()
    print("多进程执行完毕！")
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(unverifiedQueue))


    # unverifiedQueueIsEmpty = False
    # while not unverifiedQueueIsEmpty:
    #     if TaskQueue.isVerificationQueueEmpty():
    #         unverifiedQueueIsEmpty = True
    #     else:
    #         print(TaskQueue.getVerificationQueue().get())

    ProxyRedis.start()

# async def main(queue):
#     with cf.ThreadPoolExecutor(max_workers=6) as executor:
#         HttpbinObj = HttpbinWorkThread(queue)
#         loop = asyncio.get_event_loop()
#         futures = (
#             loop.run_in_executor(
#                 executor,
#                 HttpbinWorkThread(queue).run,
#             )
#         )
#         await asyncio.gather(*futures)

if __name__ == '__main__':
    startSpider()