#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class ElementType(object):
    """
    COMMENT SECTION


    """
    CONTROLLER = 1
    CLOUD = 2
    CLIENT = 3
    LOGGER = 4
    SINK = 5

    _VALUES_TO_NAMES = {
        1: "CONTROLLER",
        2: "CLOUD",
        3: "CLIENT",
        4: "LOGGER",
        5: "SINK",
    }

    _NAMES_TO_VALUES = {
        "CONTROLLER": 1,
        "CLOUD": 2,
        "CLIENT": 3,
        "LOGGER": 4,
        "SINK": 5,
    }


class ElementState(object):
    WAITING = 11
    RUNNING = 12
    RESET = 13
    STOP = 14
    READY = 15

    _VALUES_TO_NAMES = {
        11: "WAITING",
        12: "RUNNING",
        13: "RESET",
        14: "STOP",
        15: "READY",
    }

    _NAMES_TO_VALUES = {
        "WAITING": 11,
        "RUNNING": 12,
        "RESET": 13,
        "STOP": 14,
        "READY": 15,
    }


class LogType(object):
    MESSAGE = 0
    PERFORMANCE = 1
    SPECS = 2

    _VALUES_TO_NAMES = {
        0: "MESSAGE",
        1: "PERFORMANCE",
        2: "SPECS",
    }

    _NAMES_TO_VALUES = {
        "MESSAGE": 0,
        "PERFORMANCE": 1,
        "SPECS": 2,
    }


class ElementConfiguration(object):
    """
    Attributes:
     - type
     - ip
     - port
     - id
     - state
     - architecture
     - tensorflow_type
     - model_id
     - test_id

    """


    def __init__(self, type=None, ip=None, port=None, id=None, state=None, architecture=None, tensorflow_type=None, model_id=None, test_id=None,):
        self.type = type
        self.ip = ip
        self.port = port
        self.id = id
        self.state = state
        self.architecture = architecture
        self.tensorflow_type = tensorflow_type
        self.model_id = model_id
        self.test_id = test_id

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.ip = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.port = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.state = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.architecture = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.STRING:
                    self.tensorflow_type = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.STRING:
                    self.model_id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 9:
                if ftype == TType.STRING:
                    self.test_id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('ElementConfiguration')
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.I32, 1)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        if self.ip is not None:
            oprot.writeFieldBegin('ip', TType.STRING, 2)
            oprot.writeString(self.ip.encode('utf-8') if sys.version_info[0] == 2 else self.ip)
            oprot.writeFieldEnd()
        if self.port is not None:
            oprot.writeFieldBegin('port', TType.I32, 3)
            oprot.writeI32(self.port)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 4)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.state is not None:
            oprot.writeFieldBegin('state', TType.I32, 5)
            oprot.writeI32(self.state)
            oprot.writeFieldEnd()
        if self.architecture is not None:
            oprot.writeFieldBegin('architecture', TType.STRING, 6)
            oprot.writeString(self.architecture.encode('utf-8') if sys.version_info[0] == 2 else self.architecture)
            oprot.writeFieldEnd()
        if self.tensorflow_type is not None:
            oprot.writeFieldBegin('tensorflow_type', TType.STRING, 7)
            oprot.writeString(self.tensorflow_type.encode('utf-8') if sys.version_info[0] == 2 else self.tensorflow_type)
            oprot.writeFieldEnd()
        if self.model_id is not None:
            oprot.writeFieldBegin('model_id', TType.STRING, 8)
            oprot.writeString(self.model_id.encode('utf-8') if sys.version_info[0] == 2 else self.model_id)
            oprot.writeFieldEnd()
        if self.test_id is not None:
            oprot.writeFieldBegin('test_id', TType.STRING, 9)
            oprot.writeString(self.test_id.encode('utf-8') if sys.version_info[0] == 2 else self.test_id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ModelConfiguration(object):
    """
    Attributes:
     - model_name
     - split_layer

    """


    def __init__(self, model_name=None, split_layer=None,):
        self.model_name = model_name
        self.split_layer = split_layer

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.model_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I16:
                    self.split_layer = iprot.readI16()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('ModelConfiguration')
        if self.model_name is not None:
            oprot.writeFieldBegin('model_name', TType.STRING, 1)
            oprot.writeString(self.model_name.encode('utf-8') if sys.version_info[0] == 2 else self.model_name)
            oprot.writeFieldEnd()
        if self.split_layer is not None:
            oprot.writeFieldBegin('split_layer', TType.I16, 2)
            oprot.writeI16(self.split_layer)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Test(object):
    """
    Attributes:
     - is_test
     - number_of_images
     - edge_batch_size
     - cloud_batch_size

    """


    def __init__(self, is_test=None, number_of_images=None, edge_batch_size=None, cloud_batch_size=None,):
        self.is_test = is_test
        self.number_of_images = number_of_images
        self.edge_batch_size = edge_batch_size
        self.cloud_batch_size = cloud_batch_size

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.BOOL:
                    self.is_test = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.number_of_images = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I16:
                    self.edge_batch_size = iprot.readI16()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I16:
                    self.cloud_batch_size = iprot.readI16()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Test')
        if self.is_test is not None:
            oprot.writeFieldBegin('is_test', TType.BOOL, 1)
            oprot.writeBool(self.is_test)
            oprot.writeFieldEnd()
        if self.number_of_images is not None:
            oprot.writeFieldBegin('number_of_images', TType.I32, 2)
            oprot.writeI32(self.number_of_images)
            oprot.writeFieldEnd()
        if self.edge_batch_size is not None:
            oprot.writeFieldBegin('edge_batch_size', TType.I16, 3)
            oprot.writeI16(self.edge_batch_size)
            oprot.writeFieldEnd()
        if self.cloud_batch_size is not None:
            oprot.writeFieldBegin('cloud_batch_size', TType.I16, 4)
            oprot.writeI16(self.cloud_batch_size)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Configuration(object):
    """
    Attributes:
     - elements_configuration

    """


    def __init__(self, elements_configuration=None,):
        self.elements_configuration = elements_configuration

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.elements_configuration = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = ElementConfiguration()
                        _elem5.read(iprot)
                        self.elements_configuration.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Configuration')
        if self.elements_configuration is not None:
            oprot.writeFieldBegin('elements_configuration', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.elements_configuration))
            for iter6 in self.elements_configuration:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Image(object):
    """
    Attributes:
     - id
     - arr_bytes
     - data_type
     - shape

    """


    def __init__(self, id=None, arr_bytes=None, data_type=None, shape=None,):
        self.id = id
        self.arr_bytes = arr_bytes
        self.data_type = data_type
        self.shape = shape

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.id = []
                    (_etype10, _size7) = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.id.append(_elem12)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.arr_bytes = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.data_type = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.shape = []
                    (_etype16, _size13) = iprot.readListBegin()
                    for _i17 in range(_size13):
                        _elem18 = iprot.readI16()
                        self.shape.append(_elem18)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Image')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.LIST, 1)
            oprot.writeListBegin(TType.STRING, len(self.id))
            for iter19 in self.id:
                oprot.writeString(iter19.encode('utf-8') if sys.version_info[0] == 2 else iter19)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.arr_bytes is not None:
            oprot.writeFieldBegin('arr_bytes', TType.STRING, 2)
            oprot.writeBinary(self.arr_bytes)
            oprot.writeFieldEnd()
        if self.data_type is not None:
            oprot.writeFieldBegin('data_type', TType.STRING, 3)
            oprot.writeString(self.data_type.encode('utf-8') if sys.version_info[0] == 2 else self.data_type)
            oprot.writeFieldEnd()
        if self.shape is not None:
            oprot.writeFieldBegin('shape', TType.LIST, 4)
            oprot.writeListBegin(TType.I16, len(self.shape))
            for iter20 in self.shape:
                oprot.writeI16(iter20)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class FileChunk(object):
    """
    Attributes:
     - data
     - remaining

    """


    def __init__(self, data=None, remaining=None,):
        self.data = data
        self.remaining = remaining

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.data = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.remaining = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('FileChunk')
        if self.data is not None:
            oprot.writeFieldBegin('data', TType.STRING, 1)
            oprot.writeBinary(self.data)
            oprot.writeFieldEnd()
        if self.remaining is not None:
            oprot.writeFieldBegin('remaining', TType.I64, 2)
            oprot.writeI64(self.remaining)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Message(object):
    """
    Attributes:
     - timestamp
     - id
     - element_type
     - message

    """


    def __init__(self, timestamp=None, id=None, element_type=None, message=None,):
        self.timestamp = timestamp
        self.id = id
        self.element_type = element_type
        self.message = message

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.DOUBLE:
                    self.timestamp = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.element_type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Message')
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.DOUBLE, 1)
            oprot.writeDouble(self.timestamp)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 2)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.element_type is not None:
            oprot.writeFieldBegin('element_type', TType.I32, 3)
            oprot.writeI32(self.element_type)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 4)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class PerformanceMessage(object):
    """
    Attributes:
     - timestamp
     - id
     - element_type
     - no_images_predicted
     - list_ids
     - elapsed_time
     - decoded_ids
     - output_dimension

    """


    def __init__(self, timestamp=None, id=None, element_type=None, no_images_predicted=None, list_ids=None, elapsed_time=None, decoded_ids=None, output_dimension=None,):
        self.timestamp = timestamp
        self.id = id
        self.element_type = element_type
        self.no_images_predicted = no_images_predicted
        self.list_ids = list_ids
        self.elapsed_time = elapsed_time
        self.decoded_ids = decoded_ids
        self.output_dimension = output_dimension

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.DOUBLE:
                    self.timestamp = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.element_type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I16:
                    self.no_images_predicted = iprot.readI16()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.list_ids = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.DOUBLE:
                    self.elapsed_time = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.STRING:
                    self.decoded_ids = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.LIST:
                    self.output_dimension = []
                    (_etype24, _size21) = iprot.readListBegin()
                    for _i25 in range(_size21):
                        _elem26 = iprot.readI16()
                        self.output_dimension.append(_elem26)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('PerformanceMessage')
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.DOUBLE, 1)
            oprot.writeDouble(self.timestamp)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 2)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.element_type is not None:
            oprot.writeFieldBegin('element_type', TType.I32, 3)
            oprot.writeI32(self.element_type)
            oprot.writeFieldEnd()
        if self.no_images_predicted is not None:
            oprot.writeFieldBegin('no_images_predicted', TType.I16, 4)
            oprot.writeI16(self.no_images_predicted)
            oprot.writeFieldEnd()
        if self.list_ids is not None:
            oprot.writeFieldBegin('list_ids', TType.STRING, 5)
            oprot.writeString(self.list_ids.encode('utf-8') if sys.version_info[0] == 2 else self.list_ids)
            oprot.writeFieldEnd()
        if self.elapsed_time is not None:
            oprot.writeFieldBegin('elapsed_time', TType.DOUBLE, 6)
            oprot.writeDouble(self.elapsed_time)
            oprot.writeFieldEnd()
        if self.decoded_ids is not None:
            oprot.writeFieldBegin('decoded_ids', TType.STRING, 7)
            oprot.writeString(self.decoded_ids.encode('utf-8') if sys.version_info[0] == 2 else self.decoded_ids)
            oprot.writeFieldEnd()
        if self.output_dimension is not None:
            oprot.writeFieldBegin('output_dimension', TType.LIST, 8)
            oprot.writeListBegin(TType.I16, len(self.output_dimension))
            for iter27 in self.output_dimension:
                oprot.writeI16(iter27)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class SpecsMessage(object):
    """
    Attributes:
     - timestamp
     - id
     - element_type
     - spec
     - value

    """


    def __init__(self, timestamp=None, id=None, element_type=None, spec=None, value=None,):
        self.timestamp = timestamp
        self.id = id
        self.element_type = element_type
        self.spec = spec
        self.value = value

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.DOUBLE:
                    self.timestamp = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.element_type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.spec = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.value = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SpecsMessage')
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.DOUBLE, 1)
            oprot.writeDouble(self.timestamp)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 2)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.element_type is not None:
            oprot.writeFieldBegin('element_type', TType.I32, 3)
            oprot.writeI32(self.element_type)
            oprot.writeFieldEnd()
        if self.spec is not None:
            oprot.writeFieldBegin('spec', TType.STRING, 4)
            oprot.writeString(self.spec.encode('utf-8') if sys.version_info[0] == 2 else self.spec)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 5)
            oprot.writeString(self.value.encode('utf-8') if sys.version_info[0] == 2 else self.value)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class FileNotFound(TException):
    """
    Attributes:
     - description

    """


    def __init__(self, description=None,):
        self.description = description

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.description = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('FileNotFound')
        if self.description is not None:
            oprot.writeFieldBegin('description', TType.STRING, 1)
            oprot.writeString(self.description.encode('utf-8') if sys.version_info[0] == 2 else self.description)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(ElementConfiguration)
ElementConfiguration.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'type', None, None, ),  # 1
    (2, TType.STRING, 'ip', 'UTF8', None, ),  # 2
    (3, TType.I32, 'port', None, None, ),  # 3
    (4, TType.STRING, 'id', 'UTF8', None, ),  # 4
    (5, TType.I32, 'state', None, None, ),  # 5
    (6, TType.STRING, 'architecture', 'UTF8', None, ),  # 6
    (7, TType.STRING, 'tensorflow_type', 'UTF8', None, ),  # 7
    (8, TType.STRING, 'model_id', 'UTF8', None, ),  # 8
    (9, TType.STRING, 'test_id', 'UTF8', None, ),  # 9
)
all_structs.append(ModelConfiguration)
ModelConfiguration.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'model_name', 'UTF8', None, ),  # 1
    (2, TType.I16, 'split_layer', None, None, ),  # 2
)
all_structs.append(Test)
Test.thrift_spec = (
    None,  # 0
    (1, TType.BOOL, 'is_test', None, None, ),  # 1
    (2, TType.I32, 'number_of_images', None, None, ),  # 2
    (3, TType.I16, 'edge_batch_size', None, None, ),  # 3
    (4, TType.I16, 'cloud_batch_size', None, None, ),  # 4
)
all_structs.append(Configuration)
Configuration.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'elements_configuration', (TType.STRUCT, [ElementConfiguration, None], False), None, ),  # 1
)
all_structs.append(Image)
Image.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'id', (TType.STRING, 'UTF8', False), None, ),  # 1
    (2, TType.STRING, 'arr_bytes', 'BINARY', None, ),  # 2
    (3, TType.STRING, 'data_type', 'UTF8', None, ),  # 3
    (4, TType.LIST, 'shape', (TType.I16, None, False), None, ),  # 4
)
all_structs.append(FileChunk)
FileChunk.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'data', 'BINARY', None, ),  # 1
    (2, TType.I64, 'remaining', None, None, ),  # 2
)
all_structs.append(Message)
Message.thrift_spec = (
    None,  # 0
    (1, TType.DOUBLE, 'timestamp', None, None, ),  # 1
    (2, TType.STRING, 'id', 'UTF8', None, ),  # 2
    (3, TType.I32, 'element_type', None, None, ),  # 3
    (4, TType.STRING, 'message', 'UTF8', None, ),  # 4
)
all_structs.append(PerformanceMessage)
PerformanceMessage.thrift_spec = (
    None,  # 0
    (1, TType.DOUBLE, 'timestamp', None, None, ),  # 1
    (2, TType.STRING, 'id', 'UTF8', None, ),  # 2
    (3, TType.I32, 'element_type', None, None, ),  # 3
    (4, TType.I16, 'no_images_predicted', None, None, ),  # 4
    (5, TType.STRING, 'list_ids', 'UTF8', None, ),  # 5
    (6, TType.DOUBLE, 'elapsed_time', None, None, ),  # 6
    (7, TType.STRING, 'decoded_ids', 'UTF8', None, ),  # 7
    (8, TType.LIST, 'output_dimension', (TType.I16, None, False), None, ),  # 8
)
all_structs.append(SpecsMessage)
SpecsMessage.thrift_spec = (
    None,  # 0
    (1, TType.DOUBLE, 'timestamp', None, None, ),  # 1
    (2, TType.STRING, 'id', 'UTF8', None, ),  # 2
    (3, TType.I32, 'element_type', None, None, ),  # 3
    (4, TType.STRING, 'spec', 'UTF8', None, ),  # 4
    (5, TType.STRING, 'value', 'UTF8', None, ),  # 5
)
all_structs.append(FileNotFound)
FileNotFound.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'description', 'UTF8', None, ),  # 1
)
fix_spec(all_structs)
del all_structs
