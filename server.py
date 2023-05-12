import socket, threading
from nickname import randoum
import time


connections = {}
connected = []

def handle_user_connection(connection: socket.socket, address: str, username: str) -> None:
    nick = f'"###nickname###" - {username}'
    connection.send(nick.encode())
    time.sleep(0.3)
    # if len(connected) > 1:
        #broadcast(f'{username} - connected', connection, username)
    broadcast(f'###connected### - {", ".join(connected)}', username)
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                decoded = msg.decode()
                print(f'{address[0]}:{address[1]} - {decoded}')
                if decoded[0] != "/":
                    msg_to_send = f'{username} - {decoded}'
                    broadcast(msg_to_send, username)
                elif decoded == "/quit":
                    remove_connection(username)
                    break
            else:
                print("breaking in handle user connecteion")
                remove_connection(username)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(list(connections.keys())[list(connections.values()).index(connection)])
            break


def broadcast(message: str, username: str) -> None:
    for client_conn in connections.values():
        try:
            print(f"sending {message}")
            client_conn.send(message.encode())
        except Exception as e:
            print('Error broadcasting message: {e}')
            remove_connection(username)


def remove_connection(nickname: str) -> None:
    global connected
    connections[nickname].close()
    connections.pop(nickname, None)
    connected.remove(nickname)
    broadcast(f'###connected### - {", ".join(connected)}', nickname)
    print(f"{nickname} disconnected")

def server() -> None:
    global connected
    LISTENING_PORT = 13000
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(10)

        print('Server running!')
        
        while True:
            # Accept client connection
            socket_connection, address = socket_instance.accept()
            username = randoum()
            print("new connection")
            connections.update({username: socket_connection})
            connected.append(username)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address, username]).start()

    except Exception as e:
        print("exception server()")
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        print("finally server()")
        if len(connections) > 0:
            for conn in connections:
                conn.close()

        socket_instance.close()


if __name__ == "__main__":
    server()