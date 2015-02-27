from __future__ import absolute_import

from ..parser import read_key_value
from ..parser import read_short
from ..parser import write_key_value
from ..parser import write_number
from .base import BaseMessage
from .common import PROTOCOL_VERSION
from .types import Types


class InitRequestMessage(BaseMessage):
    """Initialize a connection to a TChannel server."""
    message_type = Types.INIT_REQ
    VERSION_SIZE = 2
    NH_SIZE = 2
    HEADER_SIZE = 2

    HOST_PORT = 'host_port'
    PROCESS_NAME = 'process_name'

    # Micro-optimizations are the best kinds of optimizations
    __slots__ = (
        'version',
        'headers',
    )

    def parse(self, payload, size):
        self.version = read_short(payload)
        self.headers = {}

        payload.read(self.NH_SIZE)  # we don't use nh currently
        offset = 4  # 2 bytes for version, 2 bytes for nh

        while offset < size:
            header_name, header_value, bytes_read = read_key_value(
                payload,
                self.HEADER_SIZE,
            )
            offset += bytes_read
            self.headers[header_name] = header_value

    def serialize(self, out):
        out.extend(write_number(PROTOCOL_VERSION, self.VERSION_SIZE))
        out.extend(write_number(len(self.headers), self.NH_SIZE))
        for key, value in self.headers.items():
            out.extend(write_key_value(key, value, key_size=self.HEADER_SIZE))
