import socket, traceback

host = '172.20.10.3'
port = 5555
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

def main():
    while True:
        try:
            message, address = s.recvfrom(8192)
            print(message)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

if __name__ == '__main__':
try:
main()
except KeyboardInterrupt:
destroy()