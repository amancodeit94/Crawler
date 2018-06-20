
import heapq
import logging
import threading
import time

try:
    from UserDict import DictMixin
except ImportError:
    from collections import Mapping as DictMixin
from .token_bucket import Bucket
from six.moves import queue as Queue

logger = logging.getLogger('scheduler')

try:
    cmp
except NameError:
    cmp = lambda x, y: (x > y) - (x < y)


class AtomInt(object):
    __value__ = 0
    __mutex__ = threading.RLock()

    @classmethod
    def get_value(cls):
        cls.__mutex__.acquire()
        cls.__value__ = cls.__value__ + 1
        value = cls.__value__
        cls.__mutex__.release()
        return value


            heappush(self.queue, item)
            self.queue_dict[item.taskid] = item

    def _get(self, heappop=heapq.heappop):
        while self.queue:
            item = heappop(self.queue)
            if item.taskid is None:
                continue
            self.queue_dict.pop(item.taskid, None)
            return item
        return None

    @property
    def top(self):
        while self.queue and self.queue[0].taskid is None:
            heapq.heappop(self.queue)
        if self.queue:
            return self.queue[0]
        return None

    def _resort(self):
        heapq.heapify(self.queue)

    def __contains__(self, taskid):
        return taskid in self.queue_dict

    def __getitem__(self, taskid):
        return self.queue_dict[taskid]

    def __setitem__(self, taskid, item):
        assert item.taskid == taskid
        self.put(item)

    @property
    def rate(self):
        return self.bucket.rate

    @rate.setter
    def rate(self, value):
        self.bucket.rate = value

    @property
    def burst(self):
        re
            self.priority_queue.put(task)
        self.mutex.release()

    def _check_processing(self):
        now = time.time()
        self.mutex.acquire()
        while self.p
        self.mutex.release()

    def put(self, taskid, priority=0, exetime=0):
        """
