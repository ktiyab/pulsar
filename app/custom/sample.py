import time

class Greeting(object):
    def __init__(self):
        pass

    @staticmethod
    def get(name):
        return "Hello {}".format(name)

    @staticmethod
    def getSerhat(name):
        return "Hello {}".format(name)

    @staticmethod
    def sleeper(sec):
        time.sleep(int(sec))
