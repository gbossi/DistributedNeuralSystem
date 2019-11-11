import enum


def get_thrift_enum_name(enum):
    return ThriftEnum(enum).name


class ThriftEnum(enum.Enum):
    CONTROLLER = 1
    CLOUD = 2
    CLIENT = 3
    LOGGER = 4
    SINK = 5
    WAITING = 11
    RUNNING = 12
    RESET = 13
    STOP = 14
