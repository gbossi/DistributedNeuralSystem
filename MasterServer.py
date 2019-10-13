from utils.thrift_servers import Server, ServerType
from interfaces import ControllerInterface, LogInterface
from ttypes import ElementConfiguration, ElementType, ElementState
from ServerComponents.ControllerServer import ControllerInterfaceService
from ServerComponents.LogServer import LogServerInterfaceService
from thrift.TMultiplexedProcessor import TMultiplexedProcessor


if __name__ == '__main__':
    processor = TMultiplexedProcessor()

    controller_service = ControllerInterfaceService()
    id_controller = controller_service.register_element(
        ElementConfiguration(ElementType.CONTROLLER, ip='localhost', port=10100))

    logger_service = LogServerInterfaceService()
    id_logger = controller_service.register_element(
        ElementConfiguration(ElementType.LOGGER, ip='localhost', port=10100))

    processor.registerProcessor("Controller", ControllerInterface.Processor(controller_service))
    processor.registerProcessor("Logger", LogInterface.Processor(logger_service))

    print("Starting Master Server \n Available services:\n- Controller Service\n- Logger Service")
    controller_service.set_state(id_controller, ElementState.RUNNING)
    controller_service.set_state(id_logger, ElementState.RUNNING)

    server = Server(ServerType.THREADED, processor, port=10100)
    server.serve()


