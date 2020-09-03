import multiprocessing
import time

class TestClass(object):
    def __init__(self):
        self.item = list()

    def separated_func(self):
        # for i in range(10):
        #     print('separated', i)
        print(self.item)

    def not_separated_func(self):
        # time.sleep(0.001)
        # for i in range(10):
        #     print('not separated', i)
        pass

obj = TestClass()
multiprocessing.Process(target=obj.separated_func).start()
obj.not_separated_func()