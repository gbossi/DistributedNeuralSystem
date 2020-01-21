import argparse
import sys
sys.path.append("gen-py")

from src.system_elements.remote_edge_lite import remote_edge_lite_main
from src.system_elements.controller import controller_main


parser = argparse.ArgumentParser(description='welcome')
parser.add_argument('--element_type', '-e', choices=['edge-lite', 'controller'], required=True,
                        help='available types: edge-lite, controller "')
parser.add_argument('--master-ip', '-mip', required=True,
                    help='define the ip of the master server i.e. 192.168.1.125"')
parser.add_argument('--master-port', '-mpo', required=True,
                    help='define the port of the master server i.e. 10100"', type=int)
parser.add_argument('--images-source', '-ims',
                    help='folder containing the input images"')
parser.add_argument('--test-source', '-tst',
                    help='csv file containing the test configurations')
args = parser.parse_args()

element_type = args.element_type
master_ip = args.master_ip
master_port = args.master_port
images_source = args.images_source
test_source = args.test_source

if element_type in ['edge-lite', 'controller'] and not (master_ip and master_port):
    parser.error('master server description is required')
if element_type == 'controller' and not test_source:
    test_source = 'notest'

if element_type == 'edge-lite':
    remote_edge_lite_main(master_ip, master_port)
elif element_type == 'controller':
    controller_main(master_ip, master_port, test_source)

