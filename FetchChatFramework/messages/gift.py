import time

from . import message_pb2
from .base import Base


class GiftMessage(Base):
    def __init__(self):
        self.instance = message_pb2.GiftMessage()

#    def format_content(self):
#        return self.user().nickname + ': ' + self.instance.content

#    def __str__(self):
#        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【发言】' + self.format_content()
