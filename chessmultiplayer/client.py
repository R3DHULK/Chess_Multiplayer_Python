import socket
import chess
import threading

def receive_and_display_board(client_socket):
    while True:
        data = client_socket.recv(4096).decode()
        if not data:
            break

        print(data)

        if data.startswith("Game Over"):
            break

    client_socket.close()

def send_move(client_socket):
    while True:
        move = input("Enter your move (e.g., e2e4): ")
        client_socket.sendall(move.encode())

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("SERVER_IP_ADDRESS", 8080))  # Replace SERVER_IP_ADDRESS with the server's IP address

    receive_thread = threading.Thread(target=receive_and_display_board, args=(client_socket,))
    receive_thread.start()

    send_move(client_socket)
