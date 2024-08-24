import socketpool
import wifi

wifi.radio.connect("Ejemplo","12345678")
pool=socketpool.SocketPool(wifi.radio)

print("wifi.radio",wifi.radio.hostname, wifi.radio.ipv4_address)
s = pool.socket()
s.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  buffer = bytearray(1024)  # Create a mutable buffer
  bytes_received, address = conn.recvfrom_into(buffer)  # Receive data into the buffer and get the sender's address
  print("Received from:", address)
  print("Received data:", buffer[:bytes_received]) 
  response = """
<!DOCTYPE html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
"""
  conn.send(response)
  conn.close()
