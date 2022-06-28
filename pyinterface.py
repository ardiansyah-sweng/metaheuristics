from abc import ABC, abstractmethod

class Phone(ABC):
    @abstractmethod
    def voice(self):
        pass

class Text(ABC):
    @abstractmethod
    def textMessage(self):
        pass

class Camera(ABC):
    @abstractmethod
    def photo():
        print('poto')

class BestMobilePhoneEver:
    def selector(type):
        if (type == 1):
            print('ini')
            t = Camera

bm = BestMobilePhoneEver.selector(1)