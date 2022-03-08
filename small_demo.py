# -*- coding:utf-8 -*-
import threading
import time
import typing
from datetime import timedelta, datetime
from queue import Queue
from threading import Lock


class container:
    def __init__(self):
        self.items = {}


class MsgQueue(object):

    def __init__(self, name: str, ):
        self.triggers = []
        self.name = name
        self.msg = Queue()
        self._lock = Lock()

    def get_msg(self):
        with self._lock:
            return self.msg.get(block=True, timeout=None)

    def add_trigger(self, trigger: "Trigger"):
        self.triggers.append(trigger)


class Trigger(object):
    def __init__(self):
        self.start_at = datetime.now()

    def generate_msg(self):
        return {'id': 1, 'msg': '111'}

    def get_next_run_time(self):
        return self.start_at


class Broker:
    def __init__(self):
        self.queue_locks = {}
        self.pool: typing.Mapping[str, MsgQueue] = {}
        # {
        #     'queue_name': {
        #         'triggers': [],
        #         'visible_data': Queue(),
        #     }
        # }

    def set_msg_queue(self, msg_queue: MsgQueue):
        self.pool[msg_queue.name] = msg_queue

    def start(self):
        self.run()

    def _start(self):
        pass

    def run(self):
        while 1:
            time.sleep(2)
            for name, msg_queue in self.pool.items():
                for trigger in msg_queue.triggers:
                    if trigger.get_next_run_time() < datetime.now():
                        msg = trigger.generate_msg()
                        msg_queue.msg.put(msg)
                        print('schedule msg')

    def get(self, queue_name):

        return self.pool.get(queue_name).get_msg()


class Consumer(object):

    def __init__(self):
        self.broker = None

    @property
    def ident(self):
        return threading.get_ident()

    def connect(self, broker):
        self.broker = broker

    def handle_msg(self, msg):
        print('msg handled: ', self.ident, msg)

    def consume(self, queue_name):
        while 1:
            msg = self.broker.get(queue_name)
            print('got msg: ', msg)
            self.handle_msg(msg)
            time.sleep(1)

    def start(self, queue_name):
        t = threading.Thread(target=self.consume, args=(queue_name,))
        t.setDaemon(daemonic=True)
        t.start()


if __name__ == '__main__':
    broker = Broker()
    queue_name = 'demo_queue'
    q = MsgQueue(name=queue_name)
    q.add_trigger(Trigger())
    broker.set_msg_queue(q)
    c = Consumer()
    c.connect(broker)
    c.start(queue_name=queue_name)
    broker.start()
