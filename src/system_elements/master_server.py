from src.utils.thrift_servers import Server, ServerType
from src.components.server_components.controller_server import ControllerInterfaceService
from src.components.server_components.log_server import LogServerInterfaceService
from thrift.TMultiplexedProcessor import TMultiplexedProcessor
from thrift_interfaces import ControllerInterface, LogInterface


def master_server_main(master_port=10100):
    processor = TMultiplexedProcessor()

    controller_service = ControllerInterfaceService()
    logger_service = LogServerInterfaceService()

    processor.registerProcessor("Controller", ControllerInterface.Processor(controller_service))
    processor.registerProcessor("Logger", LogInterface.Processor(logger_service))

    print("Starting Master Server \nAvailable services:\n- Controller Service\n- Logger Service")

    server = Server(ServerType.THREADED, processor, port=master_port)
    print("Server available at: " + server.ip + " on port " + str(server.port))

    server.serve()


if __name__ == '__main__':
    master_server_main()

