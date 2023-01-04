import socket
import os

class User:

    def __init__(self,socket: socket.socket, address: socket._RetAddress, username: str = 'Undefined-User') -> None:
        self.socket = socket
        self.address = address
        self.username = username
        self.isActive = False
    
    def initUsername(self) -> None:
        self.username = os.getlogin()
    
    def getIPv4(self) -> str:
        return self.address[0]
    
    def getPort(self) -> int:
        return self.address[1]