# Proposed Solutions to Control the RC Car via Arduino

This document outlines three potential solutions for controlling the RC car using an Arduino, followed by a feasibility analysis for each solution.

## First Solution: Replace the 2.4GHz Transceiver Chip in the Remote Controller

### Overview
In the remote controller, the chip responsible for handling the 2.4GHz communication receiver is the **XN297LBW**. It is a 2.4GHz wireless transceiver chip designed for wireless applications.
- Datasheet: [XN297LBW Datasheet](https://www.panchip.com/static/upload/file/20190916/1568621331607821.pdf)

### Proposed Approach
This solution consists of replacing the role of the XN297LBW chip and creating a new transmitter to handle data communication.

### Challenges
- This requires reverse engineering the proprietary protocol between the remote controller and the car.
- The complexity of replicating the communication protocol makes this solution less practical.

## Second Solution: Replace the Receiver in the RC Car

### Overview
The RC car contains a 2-in-1 receiver that also functions as an ESC (Electronic Speed Controller).

### Feasibility
- Replacing the receiver is not feasible since the ESC functionality is integrated into the receiver.
- The integrated nature of the receiver and ESC means we cannot directly control the ESC independently.

## Third Solution: Replace the Usage of Potentiometer Electronically

### Overview
Technically, it is possible to replace the potentiometer oin the RC command with a digital version and control it via Arduino.

#### Details
- **Current Potentiometer (5kΩ):** [Link to Potentiometer Details](https://www.elektroda.com/rtvforum/topic3377367.html)
- **Proposed Digital Potentiometer:** **X9C103S**, a 10kΩ digital potentiometer with nonvolatile memory.
  - It is controlled via an increment/decrement signal rather than an SPI interface, which means we cannot directly jump from one value to another; we need to traverse through all intermediate values.
  - The time between two values is 1 microsecond.
  - [Demonstration of Digital Potentiometer](https://www.youtube.com/watch?v=lGk_HVKXYWA)

#### How to Control a Digital Potentiometer with Arduino
- [Arduino and MCP4131 Digital Potentiometer Tutorial](https://www.youtube.com/watch?v=zQ5_NPeBfHM)
- [Arduino and Digital Potentiometer Project](https://www.hackster.io/umpheki/arduino-and-mcp4131-digitally-controlled-potentiometer-dcp-d35997)

## Final Step of Solution Selection
Initially, the first solution seemed most promising, but after extensive research, it proved impractical due to the complexity of reversing the communication protocol.

### Links Used During Research
- [Discussion on Reverse Engineering Drone Protocol](https://mmelchior.wordpress.com/2016/06/06/qc-360-a1-p1/)
- [XN297L as Transmitter and NRF24L01 as RX](https://deviationtx.com/forum/protocol-development/9024-question-xn297l-as-transmitter-and-nrf24l01-as-rx)

## Technical Considerations
### SPI Interface
- [Serial Peripheral Interface (SPI) Overview](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)

### System Architecture with Two Digital Potentiometers

#### Protocol Diagram
```
+--------------------+    Nrf24 signal for lidar data (1) +--------------------+
|        CAR         | ---------------------------------->|    Arduino PC      |
+--------------------+                                    +--------------------+
^                                                                    |
|                                                                    |
|      RF signal of the remote controller controlled by Arduino (2)  |
+--------------------------------------------------------------------+
```

- **(1)** Signal between two Arduinos: The first Arduino on the car transmits the lidar data.
- **(2)** Signal between the remote controller and the Arduino: The Arduino transmits the signal to the car, replacing the role of the potentiometer.
