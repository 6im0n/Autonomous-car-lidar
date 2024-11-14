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

# Disasembly of the Lidar

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_211520.jpg)
head removed show the lidar with IR laser and receptor

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_211525.jpg)
Same with the laser protector removed

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_211356.jpg)
Back of the lidar Show the port and the comminucation used by it

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_211431.jpg)
Explaination of the mainboard and the usage of IR communication betwen head and main board

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_211852.jpg)
detailed view of the head detached of the rest of her support


![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_212243.jpg)
Explenation of the encoder part, and the "object" that is différent size represent the reset of the angle, so the 0 angle.

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/LidarRetroEngineering/schema/20240520_212322.jpg)
Head of the lidar and the main support of the lidar
