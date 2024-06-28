from socket import timeout
import serial
import time
import threading
import sys
import signal

#Serial port variables
#Permission problems under Linus use: sudo chmod 666 /dev/ttyUSB0 
SERIAL_PORT_WIN = "COM3"
SERIAL_PORT_LINUX = '/dev/ttyACM0'
SERIAL_PORT = SERIAL_PORT_LINUX
SERIAL_BAUDRATE = 115200

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
#RANGE_SCALE = 0.25 * 0.001  #Convert received value to meters (LSB: 0.25 mm)
RANGE_SCALE = 0.25 * 1  #Convert received value to millimeters (LSB: 0.25 mm)
PRINTABLE = False

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
            #print("Angle: %f" % angle)
            #print("Distance: %f" % distance)
            lastDistance = distance
            continue
        if valuetodelete > 0 and (abs(distance - lastDistance) < 0.13):
            valuetodelete -= 1
        else :
            data.distance_tab.append(distance)
            #print("Angle: %f" % angle)
            #print("Distance: %f" % distance)
            lastDistance = distance

    #print (len(data.distance_tab))
    if len(data.distance_tab) < 32:
        data.distance_tab.clear()


def LiDARFrameProcessing(frame: Delta2GFrame):
    print("Processing Frame")
    global PRINTABLE
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
                #print(data.angle_distance_tab)

                print("1")
                print("OK")
                print("No errors so far")
                RefineValue()
                for i in range(len(data.distance_tab)):
                    print(round(data.distance_tab[i], 1))
                print("No further info")
                time.sleep(1)
                #print(len(data.distance_tab))
                data.angle_distance_tab.clear()
                data.distance_tab.clear()
        #	for i in range(len(scanSamplesRange)):
        #		angle_increment = 360.0 / SCAN_STEPS
        #		print("samplesize: %f" % len(scanSamplesRange))
        #		angle = (i * (angle_increment / len(scanSamplesRange)))
        #		print("increment: %f" % angle_increment)
        #		print("Angle: %f" % angle)

def LidarMangement():
    try:
        lidarSerial = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=0)
    except serial.serialutil.SerialException:
        print("ERROR: Serial Connection Error")
        return

    status = 0
    checksum = 0
    lidarFrame = Delta2GFrame()
    while True:
        rx = lidarSerial.read(100)
        for by in rx:
            match status:
                case 0:
                    #1st frame byte: Frame Header
                    lidarFrame.frameHeader = by
                    if lidarFrame.frameHeader == FRAME_HEADER:
                        #Valid Header
                        status = 1
                    #else:
                        #print("ERROR: Frame Header Failed") don't print this error
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

def start_simulation():
    print("Simulation started")

def stop_simulation():
    print("Simulation stopped")

def car_forward():
    print("Car moving forward")

def car_backwards():
    print("Car moving backwards")

def wheels_dir():
    print("Car wheels direction")

def get_info_lidar():
    global PRINTABLE
    PRINTABLE = True

def get_current_speed():
    print("Current speed")

def get_current_wheels():
    print("Current wheels")

def cycle_wait():
    print("Cycle wait")

def get_car_speed_max():
    print("Car speed max")

def get_car_speed_min():
    print("Car speed min")


AI_REQUEST = [
    ["START_SIMULATION", start_simulation],
    ["STOP_SIMULATION", stop_simulation],
    ["CAR_FORWARD", car_forward],
    ["CAR_BACKWARDS", car_backwards],
    ["WHEELS_DIR", wheels_dir],
    ["GET_INFO_LIDAR", get_info_lidar],
    ["GET_CURRENT_SPEED", get_current_speed],
    ["GET_CURRENT_WHEELS", get_current_wheels],
    ["CYCLE_WAIT", cycle_wait],
    ["GET_CAR_SPEED_MAX", get_car_speed_max],
    ["GET_CAR_SPEED_MIN", get_car_speed_min]
]

def signal_handler(sig, frame):
    sys.exit(0)


def main():
    LidarMangement()
"""
def main():
    signal.signal(signal.SIGINT, signal_handler)
    #lidarThread = threading.Thread(target=LidarMangement)
    #lidarThread.start()
    global PRINTABLE
    while True:
        LidarMangement()
        readline = input()
        if readline == "exit":
            break
        print(readline)
        if readline[len(readline) - 1] == '\n':
            print("The command ends with a newline")
        if any(readline == command[0] for command in AI_REQUEST):
            for command in AI_REQUEST:
                if readline == command[0]:
                    command[1]()
                    break
        else:
            print("The command is not recognized")
        PRINTABLE = False
    #lidarThread.join()
"""


if __name__ == "__main__":
    main()
