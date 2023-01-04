import socket
import json
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 1234))
print("Server started with IPv4:", socket.gethostbyname(socket.gethostname()))

with open('users.json', 'r') as file:
    user_list_json: dict = json.load(file)

def msgSend(port, msg: str, user_list: dict | socket.socket) -> None:
    if isinstance(user_list, dict):
        for user in user_list:
            if user["port"] == port:
                user["client"].send(msg.encode("utf-8"))
                break
        print("Failed to send message '{msg}' to port {port}")

    elif isinstance(user_list, socket.socket):
        user_list.send(msg.encode("utf-8"))
        
    else: raise TypeError("Incorrect 'user_list' input")

def getUsername(validated_user_list: dict, port='', user_id='') -> str:
    if user_id:
        return validated_user_list[user_id]["username"]
    
    elif port:
        for user_id in validated_user_list:
            if validated_user_list[user_id]["port"] == port:
                return validated_user_list[user_id]["username"]
        raise KeyError(f"Can't find user on port {port}")

    else: raise ValueError("'user_id' or 'port' was not specified")

def listener_func(server: socket.socket, user_list_json: dict) -> None:
    global unvalidated_client_dict, validated_user_list
    server.listen()

    #iteration = 0
    while True:
        #print(f"Iteration {iteration}")
        #iteration += 1

        full_user_list = {**unvalidated_client_dict, **validated_user_list}
        for user in full_user_list:
            msg_port, data = full_user_list[user]["client"].recv(1024).decode("utf-8").split("::")
            if data[:1] == '/':

                if not data == "/None":
                    user_id = data[1:]
                    new_user = {user_id: {**(user_list_json[user_id]), "client": unvalidated_client_dict[msg_port]["client"], "port": msg_port}}
                    
                    msgSend(msg_port, "a", unvalidated_client_dict[msg_port]["client"])
                    print(f"{user_list_json[user_id]['username']} successfull connected on {msg_port}")
                
                else:
                    user_id = str(len(user_list_json.keys()) + 1)
                    user_list_json = {**user_list_json, f"{user_id}": {"username": f"User-{user_id}", "groups": []}}
                    #print(user_list_json)
                    new_user = {
                        user_id: {
                            **(user_list_json[user_id]),
                            "client": unvalidated_client_dict[msg_port]["client"],
                            "port": msg_port
                        }
                    }

                    # save new user into json
                    with open("users.json", "w") as file:
                        json.dump(user_list_json, file)

                    msgSend(msg_port, f"r{user_id}", unvalidated_client_dict[msg_port]["client"])
                    print(f"New User-{user_id} registered and connected on {msg_port}")
                
                validated_user_list = {**validated_user_list, **new_user}

            else:
                print(f"{getUsername(validated_user_list, port=msg_port)}: {data}")

def acceptor_func(server) -> None:
    global unvalidated_client_dict
    while True:
        client, client_address = server.accept()
        unvalidated_client_dict = {**unvalidated_client_dict, str(client_address[1]): {"client": client}}

def sender_func() -> None:
    while True:
        port, msg = input("> ").split('::')
        getSocket(port, ).send(msg.encode("utf-8"))

def getSocket(port:str) -> socket.socket:
    global validated_user_list
    for user in validated_user_list:
        if validated_user_list[user]['port'] == port:
            return validated_user_list[user]['client']
    print(f'Invalid user port {port}')

unvalidated_client_dict = {}
validated_user_list     = {}

listener = Thread(target=listener_func, args=(server, user_list_json))
acceptor = Thread(target=acceptor_func, args=(server,))
sender   = Thread(target=sender_func, args=())

listener.start()
acceptor.start()
sender.start()
