import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='welcome')
parser.add_argument('--tfversion', '-tfv', choices=['lite', 'normal'], required=True,
                    help='specify the version of the app you want to use "')

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

args = parser.parse_args()
tfversion = args.tfversion

command = subprocess.run(['apt-get', 'install',
                          'lshw',
                          'libjpeg-dev',
                          'python3-pip',
                          'libatlas-base-dev',
                          'libopenjp2-7',
                          'libtiff5', '-y'],
                         stdout=subprocess.PIPE)
print(command.stdout.decode().rstrip())

command = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE)
architecture = command.stdout.decode().rstrip()

if "x86_64" in architecture or "aarch64" in architecture or "armv7l" in architecture:
    print("Processor "+architecture+" supported")
else:
    print("Processors not supported")
    exit()

command = subprocess.run(['python3', '-V'], stdout=subprocess.PIPE)
python_version = command.stdout.decode().rstrip()

version = ""

if "3.6" in python_version:
    version = "cp36-cp36m"
elif "3.7" in python_version:
    version = "cp37-cp37m"
else:
    print("Python version not supported")
    exit()

print("Python version "+version+" supported")


tensorflow_lite = "https://dl.google.com/coral/python/tflite_runtime-2.1.0-"+version+"-linux_"+architecture+".whl"

subprocess.run(['python3', '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE)

print("Installing Python dependencies")
if tfversion == 'lite':
    print("Tensorflow Lite Version selected")
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', './setup/tensorflow_lite_version_requirements.txt'],
                   stdout=subprocess.PIPE)
    subprocess.run(['python3', '-m', 'pip', 'install', tensorflow_lite], stdout=subprocess.PIPE)
else:
    print("Tensorflow Version selected")
    if architecture == "aarch64":
        print("Tensorflow compilation not granted. An error can occur.")
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', './setup/tensorflow_version_requirements.txt'], stdout=subprocess.PIPE)

print("Installation procedure complete")
