from utils.thrift_servers import Server, ServerType
from interfaces import ControllerInterface, LogInterface
from ttypes import ElementConfiguration, ElementType, ElementState
from ServerComponents.ControllerServer import ControllerInterfaceService
from ServerComponents.LogServer import LogServerInterfaceService
from thrift.TMultiplexedProcessor import TMultiplexedProcessor


if __name__ == '__main__':
    processor = TMultiplexedProcessor()

    controller_service = ControllerInterfaceService()
    logger_service = LogServerInterfaceService()

    processor.registerProcessor("Controller", ControllerInterface.Processor(controller_service))
    processor.registerProcessor("Logger", LogInterface.Processor(logger_service))

    print("Starting Master Server \nAvailable services:\n- Controller Service\n- Logger Service")
    print(controller_service.get_complete_configuration())


    server = Server(ServerType.THREADED, processor, port=10100)
    server.serve()


