import socket
import json
from threading import Thread

#DIR_PATH = "\\".join(__file__.split('\\')[:-1]) + "\\"
DIR_PATH = ''
RUNNING = True

# +-----------+
# | FUNCTIONS |
# +-----------+

def msgSend(port, msg: str, user_list: dict | socket.socket) -> None:
    if isinstance(user_list, dict):
        for user in user_list:
            if user["port"] == port:
                user["socket"].send(msg.encode("utf-8"))
                break
        print("Failed to send message '{msg}' to port {port}")

    elif isinstance(user_list, socket.socket):
        user_list.send(msg.encode("utf-8"))
        
    else: raise TypeError("Incorrect 'user_list' input")


def listener_func(server: socket.socket, user_list_json: dict) -> None:
    global unvalidated_client_dict, validated_user_list, RUNNING
    server.listen()
    while RUNNING:
        full_user_list = {**unvalidated_client_dict, **validated_user_list}
        
        for user in full_user_list:
            #print("Listen", user)
            some_shit = full_user_list[user]["socket"].recv(1024).decode("utf-8")
            #print(some_shit)
            msg_port, data = some_shit.split("::")
            
            if data[:1] == '/':
                #print(f"Starting validate {msg_port}")

                if not data == "/None":
                    user_id = data[1:]
                    new_user = {msg_port: {**(user_list_json[user_id]), "socket": unvalidated_client_dict[msg_port]["socket"], "user_id": user_id}}
                    
                    msgSend(msg_port, "a", unvalidated_client_dict[msg_port]["socket"])
                    print(f"{user_list_json[user_id]['username']} successfull connected on {msg_port}")
                
                else:
                    user_id = str(len(user_list_json.keys()) + 1)
                    user_list_json = {**user_list_json, f"{user_id}": {"username": f"User-{user_id}", "groups": []}}
                    #print(user_list_json)
                    new_user = {msg_port: {**(user_list_json[user_id]), "socket": unvalidated_client_dict[msg_port]["socket"], "user_id": user_id}}

                    # save new user into json
                    with open(f"{DIR_PATH}users.json", "w", encoding='utf-8') as file:
                        json.dump(user_list_json, file)

                    msgSend(msg_port, f"r{user_id}", unvalidated_client_dict[msg_port]["socket"])
                    print(f"New User-{user_id} registered and connected on {msg_port}")
                
                del unvalidated_client_dict[user]
                validated_user_list = {**validated_user_list, **new_user}

            else:
                print(f"{validated_user_list[msg_port]['username']}: {data}")
            
            full_user_list = {**unvalidated_client_dict, **validated_user_list}


def acceptor_func(server) -> None:
    global unvalidated_client_dict, RUNNING
    while RUNNING:
        client, client_address = server.accept()
        unvalidated_client_dict = {**unvalidated_client_dict, str(client_address[1]): {"socket": client}}


def sender_func() -> None:
    global RUNNING
    while RUNNING:
        try:
            input_data = input()
            port, msg = input_data.split('::')
            validated_user_list[port]["socket"].send(msg.encode("utf-8"))
        except KeyError:
            print(f"[EXCEPTION] <INVALID_PORT> Can't send message to {port}")
        except ValueError:
            print(f"[EXCEPTION] <INVALID_MESSAGE_SYNTAX>")
        except EOFError:
            RUNNING = False


# +------+
# | MAIN |
# +------+

if __name__ == '__main__':

    with open(f'{DIR_PATH}users.json', 'r', encoding='utf-8') as file:
        user_list_json: dict = json.load(file)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), 1234))
    print("Server started with IPv4:", socket.gethostbyname(socket.gethostname()))

    unvalidated_client_dict = {}
    validated_user_list     = {}

    listener = Thread(target=listener_func, args=(server, user_list_json))
    acceptor = Thread(target=acceptor_func, args=(server,))
    sender   = Thread(target=sender_func, args=())

    listener.start()
    acceptor.start()
    sender.start()
