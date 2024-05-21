
example of info send by the API given for the N4S project

```
LIDAR INFO: 1:OK:No errors so far:450.0:450.0:475.0:475.0:487.5:500.0:500.0:525.0:550.0:550.0:575.0:575.0:575.0:600.0:600.0:600.0:625.0:625.0:625.0:675.0:675.0:675.0:675.0:700.0:700.0:700.0:750.0:750.0:750.0:800.0:800.0:800.0:No further info
```

### value distance contain 32 information but no angle
the angle of total FOV is  60 degrees, first-person viewpoint

The API has a 60 degres FOV and 32 values, so each value is 60/32 = 1.875 degrees of precision

The lidar on the other part for same 60 degrees FOV has 57 values, so each value is 60/57 = 1.0526 degrees of precision

### value distance contain 32 information and angle



# Disasembly of the Lidar

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211520.jpg)
head removed show the lidar with IR laser and receptor

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211525.jpg)
Same with the laser protector removed

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211356.jpg)
Back of the lidar Show the port and the comminucation used by it

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211431.jpg)
Explaination of the mainboard and the usage of IR communication betwen head and main board

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_211852.jpg)
detailed view of the head detached of the rest of her support


![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_212243.jpg)
Explenation of the encoder part, and the "object" that is différent size represent the reset of the angle, so the 0 angle.

![alt text](https://github.com/6im0n/Autonomous-car-lidar/blob/main/Lidar/schema/20240520_212322.jpg)
Head of the lidar and the main support of the lidar
