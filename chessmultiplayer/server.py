import socket
import threading
import chess
import chess.svg
import io

# Define a function to handle a single client
def handle_client(conn, addr, game):
    conn.sendall(b"Welcome to the Chess Game!\n")
    conn.sendall(chess.svg.board(board=game).encode())

    while True:
        try:
            data = conn.recv(1024).strip().decode()
            move = chess.Move.from_uci(data)

            if move in game.legal_moves:
                game.push(move)
                svg_board = chess.svg.board(board=game)
                conn.sendall(svg_board.encode())
            else:
                conn.sendall(b"Invalid move. Try again.\n")

            if game.is_game_over():
                result = game.result()
                conn.sendall(f"Game Over. Result: {result}\n".encode())
                break

        except:
            conn.sendall(b"Invalid input. Try again.\n")

    conn.close()

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8080))
server_socket.listen(2)

print("Waiting for connections...")

game = chess.Board()

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    if threading.activeCount() <= 3:  # Limit to two players
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, game.copy()))
        client_thread.start()
    else:
        conn.sendall(b"Game is full. Try again later.\n")
        conn.close()
