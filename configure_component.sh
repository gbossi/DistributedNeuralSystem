#!/usr/bin/env bash

read architecture < <(uname -p)
read pyversion < <(python3 -V)

echo "Machine Architecture: $architecture"
echo "Python Version: $pyversion"
if [[ $pyversion == *"3.6"* ]]; then
  echo "cp36-cp36m" | read pyset
  else
  if [[ $pyversion == *"3.7"* ]]; then
    echo "cp37-cp37m" | read pyset
  else
    echo "Python Version Not Supported"
    exit
  fi
fi

echo "https://dl.google.com/coral/python/tflite_runtime-2.1.0-$pyset-linux_$architecture.whl" | read tensorflow_lite_wheel
echo ${tensorflow_lite_wheel}



if [ $1 == lite ] ; then
  echo "Starting to install Tensorflow Lite Version in this machine"
else
  echo "Starting to install Tensorflow Complete Version in this machine"
fi
echo $1

echo ${architecture}