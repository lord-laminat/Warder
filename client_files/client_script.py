import json
import yadisk
import socket
#import os
from datetime import datetime
from time import time
from mss import mss
from threading import Thread

#DIR_PATH = "\\".join(__file__.split('\\')[:-1]) + "\\"
DIR_PATH = ''
RUNNING = True

def mkdir(disk: yadisk.YaDisk, full_path: str) -> None:
    path = 'disk:'
    for obj in full_path.split('/'):
        if obj == 'disk:': continue

        path += f'/{obj}'
        try:
            disk.mkdir(path)
        except yadisk.exceptions.PathExistsError:
            ... 

def userValidate(port: str) -> None:
    client.send(f"{port}::/{configs['client_id']}".encode("utf-8"))
    print("Starting validation...")
    while True:
        data: str = client.recv(1024).decode("utf-8")
        if data == 'a':
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
    global is_screenshoter_active, RUNNING
    while RUNNING:
        try:
            if time() - last_time >= configs["screenshot_delay_seconds"] and is_screenshoter_active:
                with mss() as file:
                    file.shot()

                # upload to "disk:/warden/<login>/screenshots/<date>/<>
                disk.upload("monitor-1.png", f"disk:/warder/{configs['username']}/screenshots/{str(datetime.now()).split()[0]}/screenshot_{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}.png")
                
                print(f"Screenshot {datetime.now().hour}-{datetime.now().minute}-{datetime.now().second} uploaded!")
                last_time = time()

        except Exception as ex_: client.send((f"{port}::[EXCEPTION]:\n{ex_}").encode('utf-8'))

def main(client: socket.socket, configs: dict, port: str) -> None:
    global is_screenshoter_active, RUNNING
    while RUNNING:
        data: str = client.recv(1024).decode("utf-8")
        if data == '1':
            if is_screenshoter_active:
                client.send((f"{port}::Screenshoter {configs['client_id']} is already working").encode('utf-8'))
            else:
                is_screenshoter_active = True
                try: 
                    screenshoter.start()
                except: ...
                client.send((f"{port}::Screenshoter {configs['client_id']} is launched successfully").encode('utf-8'))

        elif data == '0':
            if not is_screenshoter_active:
                client.send((f"{port}::Screenshoter {configs['client_id']} is already stopped").encode('utf-8'))
            else:
                is_screenshoter_active = False
                client.send((f"{port}::Screenshoter {configs['client_id']} is stopped successfully").encode('utf-8'))
                print("[Server]: Screenshoter was stopped by host")
        
        elif data == 'e':
            RUNNING = False
            client.send((f"{port}::Client {configs['client_id']} successfully stopped").encode('utf-8'))
            exit()
        else:
            print(f"[Server]: {data}")


if __name__ == '__main__':
    with open(DIR_PATH + 'configs.json', 'r', encoding='utf-8') as file:
        configs = json.load(file)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((configs["host_IPv4"], 1234))
    except ConnectionRefusedError as e:
        print(e)
        exit()

    port = client.getsockname()[1]
    disk = yadisk.YaDisk(token=configs["disk_token"])
    is_screenshoter_active = False

    screenshoter = Thread(target=screenshotTaker, args=(disk, time()))
    listener     = Thread(target=main, args=(client, configs, port))

    userValidate(port)
    mkdir(disk, f"disk:/warder/{configs['username']}/screenshots/{str(datetime.now()).split()[0]}/")

    listener.start()