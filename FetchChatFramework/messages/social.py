import time

from . import message_pb2
from .base import Base


class SocialMessage(Base):
    def __init__(self):
        self.instance = message_pb2.SocialMessage()