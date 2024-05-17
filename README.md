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
### Scenario 1: Limited Edge Computing (Low Power Device)
Setup: We deploy a low-power single-board computer (Raspberry Pi) at the edge to collect sensor data and process a small part of the DNN effeciently.
Data Processing: A great part of unprocessed data will be sent to the Cloud server.
Computing Power Edge: Since the limited on-device processing, it will relies heavily on cloud-based resources.

### Scenario 2: Moderate Edge Computing (Mid-Range Device)
Setup: We deploy a device with moderate processing power at the edge, like a single-board computer . This allows to process a greater part of the DNN effeciently.
Data Processing: Pre-processed data is sent to the central server, reducing the amount of raw data transferred.
Computing Power Edge: Balance between on-device processing and cloud-based analysis.

### Scenario 3: High Edge Computing (High-Power Device)
Setup: We deploy a powerful device at the edge, like a dedicated GPU graphic card. This allows for running most of the DNN layers directly on the edge device.
Data Processing: Minimal data transfer to the central server, focusing on data synchronization and remote monitoring.
Computing Power Edge: Primarily relies on on-device processing for DNN computation.

<p align="middle">
<img src="https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/8a5beaac-e217-49de-8335-ee741cc98399" width="600">
</p>

### Expected Outcomes:
We expect to see a correlation between increasing computing power at the edge and improved amount of processed image per seconds.
Scenario 3 might achieve faster response times and more tailored recommendations due to on-device AI processing.
Scenarios 1 and 2 might face limitations in real-time analysis and complex modeling due to reliance on the central server.


## Results
To prove the expected outcomes the DNN have been cut in all possible ways, to divide the computing efforts between the Edge computer and the Cloud computer accordingly.
In the next graphs, the computing time for each the results of this study is presented for each cut. The expected outcomes is confirmed.

![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/749ee5e5-070c-4a45-ba45-11c96fa8c7d3)


![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/4e88e5e5-e307-48cb-9272-69f5a9c460f6)


![image](https://github.com/gbossi/DistributedNeuralSystem/assets/38566530/45acc3b8-eb79-4e25-a542-6a32faa15fd3)

