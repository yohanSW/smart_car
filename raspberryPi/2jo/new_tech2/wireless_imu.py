import socket, traceback
import serial
import subprocess

ser = serial.Serial("/dev/ttyACM0",115200)
Gosignal = 'G'
host = '192.168.0.118'
port = 5555
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
            
str_com_1 = "cd /home/pi/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/mjpg-streamer/mjpg-streamer"
str_com_2 = "sudo make USE_LIBV4L2=true clean all"
str_com_3 = "sudo make DESTDIR=/usr install"
str_com_4 = "sh start.sh"

subprocess.check_output(str_com_1,shell=True)
subprocess.check_output(str_com_2,shell=True)
subprocess.check_output(str_com_3,shell=True)
subprocess.check_output(str_com_4,shell=True)
            
def main():
    for i in range(5):
        message, address = s.recvfrom(8192)

    while True:
        try:
            message, address = s.recvfrom(8192)
            #print(str(message))
            x = float(str(message).split(',')[6])
            y = float(str(message).split(',')[7])
            z = float(str(message).split(',')[8])
            ser_str = '#' + str(x) + ',' + str(y) + ',' + str(z)
            #print(ser_str)
            #if ser.readable() :
            #    Gosignal = ser.readline()
            #    print("sig: ", Gosignal)
            #if Gosignal == 'G\r\n' :
    	    print(ser_str)
            ser.flush()
            ser.write(str.encode(ser_str))
	        #Gosignal = 'B'
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
