import json
import yadisk
import socket
import os
from datetime import datetime
from time import time
import utils
from mss import mss
from threading import Thread

with open('configs.json', 'r') as file:
    configs = json.load(file)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((configs["host_IPv4"], 1234))
disk = yadisk.YaDisk(token=configs["disk_token"])

def userValidate(port):
    client.send(f"{port}::/{configs['client_id']}".encode("utf-8"))
    print("Starting validation...")
    while True:
        data: str = client.recv(1024).decode("utf-8")
        if data == 'a':
            client.send((f"{port}::Client "+str(configs["client_id"])+" is now active").encode('utf-8'))
            break

        elif data[:1] == 'r':
            configs["client_id"] = data[1:]
            with open("configs.json", "w") as file:
                json.dump(configs, file)
            client.send((f"{port}::Client "+str(configs["client_id"])+" successfully registered").encode('utf-8'))
            break
        
        else:
            client.send((f"{port}::Client "+str(configs["client_id"])+" has not passed validation yet").encode('utf-8'))

def screenshotTaker(disk: yadisk.YaDisk, last_time: float) -> None:
    while True:
        if time() - last_time >= configs["screenshot_delay_seconds"]:
            with mss() as file:
                file.shot()

            # upload to "disk:/warden/<login>/screenshots/<date>/<>
            disk.upload("monitor-1.png", f"disk:/warden/{os.getlogin()}/screenshots/{str(datetime.now()).split()[0]}/screenshot_{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}.png")
            print(f"Screenshot {datetime.now().hour}-{datetime.now().minute}-{datetime.now().second} uploaded!")
            last_time = time()

def main(client: socket.socket, configs: dict, port: str):
    while True:
        data: str = client.recv(1024).decode("utf-8")
        if data == '1':
            if screenshoter.is_alive():
                client.send((f"{port}::Screenshoter "+str(configs["client_id"])+" is already working").encode('utf-8'))
            else:
                screenshoter.start()
                client.send((f"{port}::Screenshoter "+str(configs["client_id"])+" is launched successfully").encode('utf-8'))

        elif data == '0':
            if not screenshoter.is_alive():
                client.send((f"{port}::Screenshoter "+str(configs["client_id"])+" is already stopped").encode('utf-8'))
            else:
                screenshoter.join()
                client.send((f"{port}::Screenshoter "+str(configs["client_id"])+" is stopped successfully").encode('utf-8'))
        
        elif data == 'e':
            screenshoter.join()
            sender.join()
            client.send((f"{port}::Client "+str(configs["client_id"])+" successfully stopped").encode('utf-8'))
            exit()
        else:
            print(f"New server's message:\n{data}")

def sender_func(client: socket.socket, port: str | int) -> None:
    while True:
        try:
            client.send(f"{port}::{input('> ')}".encode("utf-8"))
        except ValueError:
            print("[EXCEPTION] Incorrect message syntax")

port = client.getsockname()[1]

screenshoter = Thread(target=screenshotTaker, args=(disk, time()))
listener     = Thread(target=main, args=(client, configs, port))
sender       = Thread(target=sender_func, args=(client, port))

# validation 
userValidate(port)
utils.reposSetup(disk)

listener.start()
sender.start()