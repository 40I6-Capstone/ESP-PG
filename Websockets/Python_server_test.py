import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1234  # Arbitrary non-privileged port

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to a public host, and a well-known port
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port {PORT}...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Client connected from {client_address}")

        # Receive the message from the client
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")

        # Send a response back to the client
        response = "Hello from Python server"
        client_socket.sendall(response.encode('utf-8'))
        print(f"Sent response: {response}")

        # Close the connection
        client_socket.close()
