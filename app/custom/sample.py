class Greeting(object):
    def __init__(self):
        pass

    @staticmethod
    def get(name):
        return "Hello {}".format(name)
