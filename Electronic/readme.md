# 3 solutions:


## First solution:

In the remote controller the chip handle the 2.4GHZ communication receiver is a xn297lbw
https://www.panchip.com/static/upload/file/20190916/1568621331607821.pdf
the chip is a 2.4GHz wireless transceiver chip, which is designed for wireless applications.

this solution concist to replace the role of this chip and make a new transmiter for data


## Second solution:

repalce the the receiver in the car, impossible beacause the 2 in one receiver do not permit to access directly to the esc


## Third solution:

to replace the the usage of pentotimeter elelectronicly, technicaly is possible but how ? 
by replace the current potetiometer by a digital one, and control it by the arduino.

#### current potentionemeter 5kOhm:
https://www.elektroda.com/rtvforum/topic3377367.html

digital potentiometer:
X9C103S this is a 10kOhm digital potentiometer and nonvolatile memory to store the state og the current value
this potentiometer is not controled by a spi interface but by a simple increment and decrement signal.
so the probleme we can't jump to one value to other value directly, we need to go through all the value betwen the current value and the target value.
(the time betwen two value is 1 micro-second)
https://www.youtube.com/watch?v=lGk_HVKXYWA
kl
#### how to control a digital potentiometer from a arduino:
- https://www.youtube.com/watch?v=zQ5_NPeBfHM
- https://www.hackster.io/umpheki/arduino-and-mcp4131-digitally-controlled-potentiometer-dcp-d35997


## Final step of the selection of the solution:

at the begining of reasherch the first solution seams to be the best but after lot of reascherch this solution is a nightmare.
because we need to reverse completly the protocol used betwen the controller and the RC car. 

link used for this reascherch:
- talk about the protocol used by a small drone and reverse it to be used with and arduino
https://mmelchior.wordpress.com/2016/06/06/qc-360-a1-p1/
- 
https://deviationtx.com/forum/protocol-development/9024-question-xn297l-as-transmitter-and-nrf24l01-as-rx
[...] link to be added soon


## SPI interface
https://en.wikipedia.org/wiki/Serial_Peripheral_Interface

## two didigital potentiometer



## The protocol

+--------------------+    Nrf24 signal for lidar data (1) +--------------------+
|        CAR         | ---------------------------------->|    Arduino PC      |
+--------------------+                                    +--------------------+
^                                                                    |
|                                                                    |
|      RF signal of the remote controller controlled by arduino (2)  |
+--------------------------------------------------------------------+


(1) is the signal betwen the two arduino the first one on the car is the transmittter of the lidar data.
(2) is the signal betwen the remote controller and the arduino, the arduino is the transmitter of the signal to the car.

(2) when need component to replace the role of potentiometer