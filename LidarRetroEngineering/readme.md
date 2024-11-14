# LIDAR Overview
A LIDAR (Light Detection and Ranging) is a remote sensing method used to measure distances by illuminating the target with laser light and measuring the reflection with a sensor. It is commonly used in autonomous vehicles to create a 3D map of the surrounding environment by providing accurate distance measurements for obstacle detection and navigation.

## Example of Information Sent by the API for the N4S Project
```
LIDAR INFO: 1:OK:No errors so far:450.0:450.0:475.0:475.0:487.5:500.0:500.0:525.0:550.0:550.0:575.0:575.0:575.0:600.0:600.0:600.0:625.0:625.0:625.0:675.0:675.0:675.0:675.0:700.0:700.0:700.0:750.0:750.0:750.0:800.0:800.0:800.0:No further info
```
#### Distance Values Contain 32 Measurements but No Angles
The total Field of View (FOV) is 60 degrees from a first-person perspective.
- The API provides a 60-degree FOV with 32 distance values, resulting in a precision of **60/32 = 1.875 degrees** per measurement.
- The LIDAR, on the other hand, for the same 60-degree FOV, has 57 distance values, which means a precision of **60/57 = 1.0526 degrees** per measurement.

## Retro-Engineering of the LIDAR
The retro-engineering of the LIDAR was aided by the following link:
- [NotBlackMagic Lidar Modules](https://notblackmagic.com/bitsnpieces/lidar-modules/)

## Wiring Information
- **Red Wire:** 3.3V (directly connected to the motor)
- **Black Wire:** GND (directly connected to the motor)
- **Orange Wire:** 5V for the LIDAR
- **White Wire:** Signal for the LIDAR (connected to the RX of the ESP32)
- **Purple Wire:** GND for the LIDAR

## Disassembly of the LIDAR

![Lidar Head Removed](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211520.jpg)
*The head removed shows the LIDAR with IR laser and receiver.*

![Lidar Without Laser Protector](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211525.jpg)
*Same view with the laser protector removed.*

![Back of the LIDAR](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211356.jpg)
*Back of the LIDAR showing the ports and communication interfaces.*

![Mainboard Explanation](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211431.jpg)
*Explanation of the mainboard and the usage of IR communication between the head and the main board.*

![Detailed View of the Head](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211852.jpg)
*Detailed view of the head detached from the rest of the support.*

![Encoder Explanation](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_212243.jpg)
*Explanation of the encoder part and the different-sized objects that represent the reset of the angle, marking the 0-degree angle.*

![Head and Main Support](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_212322.jpg)
*Head of the LIDAR and its main support.*