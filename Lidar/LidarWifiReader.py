from socket import timeout
import serial
import time

#Serial port variables
#Permission problems under Linus use: sudo chmod 666 /dev/ttyUSB0
SERIAL_PORT_WIN = "COM3"
SERIAL_PORT_LINUX = '/dev/rfcomm0'
SERIAL_PORT = SERIAL_PORT_LINUX
SERIAL_BAUDRATE = 115200

import socket  # Import the socket module

# TCP connection variables
TCP_IP = '192.168.4.1'  # IP address of the ESP32 server
TCP_PORT = 4242

#Scan variables
scanSamplesSignalQuality = [0.0]
scanSamplesRange = [0.0]

#Delta-2G Frame Characteristics
#Constant Frame Parts values
FRAME_HEADER = 0xAA  #Frame Header value
PROTOCOL_VERSION = 0x01  #Protocol Version value
FRAME_TYPE = 0x61  #Frame Type value
#Scan Characteristics
SCAN_STEPS = 16  #How many steps/frames each full 360deg scan is composed of
#Received value scaling
ROTATION_SPEED_SCALE = 0.05 * 60  #Convert received value to RPM (LSB: 0.05 rps)
ANGLE_SCALE = 0.01  #Convert received value to degrees (LSB: 0.01 degrees)
RANGE_SCALE = 0.25 * 0.001  #Convert received value to meters (LSB: 0.25 mm)


#Delta-2G frame structure
class Delta2GFrame:
    frameHeader = 0  #Frame Header: 1 byte
    frameLength = 0  #Frame Length: 2 bytes, from frame header to checksum (excluded)
    protocolVersion = 0  #Protocol Version: 1 byte
    frameType = 0  #Frame Type: 1 byte
    commandWord = 0  #Command Word: 1 byte, identifier to distinguish parameters
    parameterLength = 0  #Parameter Length: 2 bytes, length of the parameter field
    parameters = [0]  #Parameter Field
    checksum = 0  #Checksum: 2 bytes


class data:
    angle_distance_tab = {0.0: 0.0}
    distance_tab = [0.0]


def RefineValue():
    valuetodelete = len(data.angle_distance_tab.values()) - 32
    lastDistance = 0
    for angle, distance in data.angle_distance_tab.items():
        if angle < 243.9 or  angle > 296.0:
            data.distance_tab.append(distance)
            print("Angle: %f" % angle)
            print("Distance: %f" % distance)
            lastDistance = distance
            continue
        if valuetodelete > 0 and (abs(distance - lastDistance) < 0.13):
            valuetodelete -= 1
        else :
            data.distance_tab.append(distance)
            print("Angle: %f" % angle)
            print("Distance: %f" % distance)
            lastDistance = distance

    print (len(data.distance_tab))
    if len(data.distance_tab) < 32:
        data.distance_tab.clear()


def LiDARFrameProcessing(frame: Delta2GFrame):
    match frame.commandWord:
        case 0xAE:
            #Device Health Information: Speed Failure
            rpm = frame.parameters[0] * ROTATION_SPEED_SCALE
            print("RPM: %f" % rpm)
        case 0xAD:
            #1st: Rotation speed (1 byte)
            rpm = frame.parameters[0] * ROTATION_SPEED_SCALE
            #print("RPM: %f" % rpm)

            #2nd: Zero Offset angle (2 bytes)
            offsetAngle = (frame.parameters[1] << 8) + frame.parameters[2]
            offsetAngle = offsetAngle * ANGLE_SCALE

            #3rd: Start angle of current data freame (2 bytes)
            startAngle = (frame.parameters[3] << 8) + frame.parameters[4]
            startAngle = startAngle * ANGLE_SCALE

            #Calculate number of samples in current frame
            sampleCnt = int((frame.parameterLength - 5) / 3)

            #Calculate current angle index of a full frame: For Delta-2G each full rotation has 15 frames
            frameIndex = int(startAngle / (360.0 / SCAN_STEPS))

            if frameIndex == 0:
                #New scan started
                scanSamplesRange.clear()
                scanSamplesSignalQuality.clear()

            #4th: LiDAR samples, each sample has: Signal Value/Quality (1 byte), Distance Value (2 bytes)
            for i in range(sampleCnt):
                signalQuality = frame.parameters[5 + (i * 3)]
                distance = (frame.parameters[5 + (i * 3) + 1] << 8) + frame.parameters[5 + (i * 3) + 2]
                scanSamplesSignalQuality.append(signalQuality)
                scanSamplesRange.append(distance * RANGE_SCALE)
                angle = (startAngle) + (i * ((360.0 / SCAN_STEPS) / sampleCnt))
                if 239.8 < angle < 300.9:
                    data.angle_distance_tab[angle] = distance * RANGE_SCALE
                    #print("---------Angle: %f" % angle)
                    #print("Distance: %f" % (distance * RANGE_SCALE))

            # Angle 270 is the front of the LIDAR

            if frameIndex == (SCAN_STEPS - 1):
                print("Scan Completed")
                #print(data.angle_distance_tab)
                RefineValue()
                print(data.distance_tab)
                #print(len(data.distance_tab))
                data.angle_distance_tab.clear()
                data.distance_tab.clear()
        #	for i in range(len(scanSamplesRange)):
        #		angle_increment = 360.0 / SCAN_STEPS
        #		print("samplesize: %f" % len(scanSamplesRange))
        #		angle = (i * (angle_increment / len(scanSamplesRange)))
        #		print("increment: %f" % angle_increment)
        #		print("Angle: %f" % angle)

    # Port number of the ESP32 server
def main():
    try:
        # Setup TCP connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((TCP_IP, TCP_PORT))
    except socket.error as e:
        print(f"ERROR: TCP Connection Error: {e}")
        return

    status = 0
    checksum = 0
    lidarFrame = Delta2GFrame()
    while True:
        try:
            rx = client_socket.recv(100)  # Read data from TCP connection
        except socket.timeout:
            print("ERROR: TCP Read Timeout")
            continue
        except socket.error as e:
            print(f"ERROR: TCP Read Error: {e}")
            break

        for by in rx:
            match status:
                case 0:
                    #1st frame byte: Frame Header
                    lidarFrame.frameHeader = by
                    if lidarFrame.frameHeader == FRAME_HEADER:
                        #Valid Header
                        status = 1
                    else:
                        print("ERROR: Frame Header Failed")
                    #Reset checksum, new frame start
                    checksum = 0
                case 1:
                    #2nd frame byte: Frame Length MSB
                    lidarFrame.frameLength = (by << 8)
                    status = 2
                case 2:
                    #3rd frame byte: Frame Length LSB
                    lidarFrame.frameLength += by
                    status = 3
                case 3:
                    #4th frame byte: Protocol Version
                    lidarFrame.protocolVersion = by
                    if lidarFrame.protocolVersion == PROTOCOL_VERSION:
                        #Valid Protocol Version
                        status = 4
                    else:
                        print("ERROR: Frame Protocol Version Failed")
                        status = 0
                case 4:
                    #5th frame byte: Frame Type
                    lidarFrame.frameType = by
                    if lidarFrame.frameType == FRAME_TYPE:
                        #Valid Frame Type
                        status = 5
                    else:
                        print("ERROR: Frame Type Failed")
                        status = 0
                case 5:
                    #6th frame byte: Command Word
                    lidarFrame.commandWord = by
                    status = 6
                case 6:
                    #7th frame byte: Parameter Length MSB
                    lidarFrame.parameterLength = (by << 8)
                    status = 7
                case 7:
                    #8th frame byte: Parameter Length LSB
                    lidarFrame.parameterLength += by
                    lidarFrame.parameters.clear()
                    status = 8
                case 8:
                    #9th+ frame bytes: Parameters
                    lidarFrame.parameters.append(by)
                    if len(lidarFrame.parameters) == lidarFrame.parameterLength:
                        #End of parameter frame bytes
                        status = 9
                case 9:
                    #N+1 frame byte: Checksum MSB
                    lidarFrame.checksum = (by << 8)
                    status = 10
                case 10:
                    #N+2 frame byte: Checksum LSB
                    lidarFrame.checksum += by
                    #End of frame reached
                    #Compare received and calculated frame checksum
                    if lidarFrame.checksum == checksum:
                        #Checksum match: Valid frame
                        LiDARFrameProcessing(lidarFrame)
                    else:
                        #Checksum missmatach: Invalid frame
                        print("ERROR: Frame Checksum Failed");
                    status = 0
            #Calculate current frame checksum, all bytes excluding the last 2, which are the checksum
            if status < 10:
                checksum = (checksum + by) % 0xFFFF

if __name__ == "__main__":
    main()
