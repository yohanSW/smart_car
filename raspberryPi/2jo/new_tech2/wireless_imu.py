import socket, traceback
#import serial


#ser = serial.Serial("/dev/ttyACM0",115200)
host = '192.168.0.113'
port = 5555
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

def main():
    for i in range(5):
        message, address = s.recvfrom(8192)
    print(str(message))
    x = float(str(message).split(',')[6])
    y = float(str(message).split(',')[7])
    z = float(str(message).split(',')[8])

    while True:
        try:
            message, address = s.recvfrom(8192)
            #print(str(message))
            changeX = float(str(message).split(',')[6])
            changeY = float(str(message).split(',')[7])
            changeZ = float(str(message).split(',')[8])
            changeX = changeX - x
            changeY = changeY - y
            changeZ = changeZ - z
            x = float(str(message).split(',')[6])
            y = float(str(message).split(',')[7])
            z = float(str(message).split(',')[8])
            print(changeX,changeY,changeZ)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

def destroy():
    return 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
