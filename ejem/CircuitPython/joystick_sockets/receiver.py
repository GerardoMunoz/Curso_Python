import wifi
import socketpool
#import adafruit_requests
import time

# Wi-Fi Configuration
SSID = "Ejemplo"  # Replace with your Wi-Fi SSID
PASSWORD = "12345678"  # Replace with your Wi-Fi password

# Server Configuration
PORT = 5000  # Must match the PORT used by the transmitter

# Connect to Wi-Fi
wifi.radio.connect(SSID, PASSWORD)
print(f"Connected to {SSID} with IP address: {wifi.radio.ipv4_address}")

# Initialize the socket
pool = socketpool.SocketPool(wifi.radio)
server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((str(wifi.radio.ipv4_address), PORT))
server_socket.listen(1)
print(f"Server listening on {wifi.radio.ipv4_address}:{PORT}")

# Wait for a connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

try:
    while True:
        # Receive the data from the client
        buffer = bytearray(1024)  # Create a mutable buffer
        bytes_received, address = client_socket.recvfrom_into(buffer)  # Receive data into the buffer and get the sender's address
        request_str = str(buffer[:bytes_received])
        print("Received from:", address)
        print("Received data:", request_str,bytes_received)

#         data = client_socket.recv(1024).decode('utf-8')
#         if not data:
#             break
#         
#         # Print the received data
#         print(f"Received: {data.strip()}")
finally:
    client_socket.close()
    server_socket.close()
