from queue import Queue


class TaskQueue(object):

    #已校验有效代理IP队列
    verificationQueue = Queue()
    #未校验有效代理IP队列
    unverifiedQueue = Queue()

    @classmethod
    def getVerificationQueue(cls):
        return cls.verificationQueue

    @classmethod
    def getUnverifiedQueue(cls):
        return cls.unverifiedQueue

    @classmethod
    def putVerificationQueue(cls, item):
        return cls.verificationQueue.put(item)

    @classmethod
    def putUnverifiedQueue(cls, item):
        return cls.unverifiedQueue.put(item)

    @classmethod
    def isVerificationQueueEmpty(cls):
        return cls.verificationQueue.empty()

    @classmethod
    def isUnverifiedQueueEmpty(cls):
        return cls.unverifiedQueue.empty()
