import socket, traceback

host = '192.168.0.113'
port = 5555
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

def main():
    message, address = s.recvfrom(8192)
    #print(str(message))
    x = float(str(message).split(',')[6])
    y = float(str(message).split(',')[7])
    z = float(str(message).split(',')[8])

    while True:
        try:
            message, address = s.recvfrom(8192)
            #print(str(message))
            changeX
            x = float(str(message).split(',')[6])
            y = float(str(message).split(',')[7])
            z = float(str(message).split(',')[8])
            print(x,y,z)
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
