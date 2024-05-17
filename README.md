# Distributed Neural System

DiNeSys is a distributed system built for deep learning network profiling on cloud-edge systems, developed with Tensorflow (CNN computational part) Apache Thrift (client/server structure).
The system supports a cluster of connected clients and coordinate their behaviors, in order to coordinate image computation. The central master server by following a stateful approach, provides a frame of reference to all the clients connected. The controller creates and monitors all the tests and the Mobile Edges and Cloud Servers jointly compute the Convolutional Neural Network.
<p align="middle">
<img src="https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/5a419df0-2a71-422d-bf2c-2d586e666e0f" width="300" hspace="40"/>
<img src="https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/1c3a63b4-7a45-4e53-bb2b-d4c699c829ed" width="300">
</p>
All the elements are connected to the master server through the log service and the controller service.
These two services provides different function to the connected elements depending on the element type, since the controller element has the task to control an experiment and to download all the log at the end, while the Mobile Edges and the Cloud Server connected to each other has the task to perform the experiment.
<p align="middle">
<img src="https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/c735dc55-c34f-4950-ab54-89ecdbe0361c" width="600">
</p>

## Experimental Scenarios

<p align="middle">
<img src="https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/8a5beaac-e217-49de-8335-ee741cc98399" width="600">
</p>


![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/749ee5e5-070c-4a45-ba45-11c96fa8c7d3)


![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/4e88e5e5-e307-48cb-9272-69f5a9c460f6)


![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/45acc3b8-eb79-4e25-a542-6a32faa15fd3)

