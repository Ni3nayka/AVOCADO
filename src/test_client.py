import socket               # Import socket module
from device.wifi_driver import get_ip
from time import sleep

s = socket.socket()         # Create a socket object
#host = "192.168.1.62" #socket.gethostname() # Get local machine name
host = get_ip()
port = 1234                 # Reserve a port for your service.

s.connect((host, port))
# s.send(b'Hi i am aslam')     
for i in range(3):
    s.send(str(str(i)+"\n").encode('utf-8'))
    sleep(0.2)
print(s.recv(1024))
print(s.recv(1024))
s.close                     # Close the socket when done     
