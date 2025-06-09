import socket

# Get the hostname
hostname = socket.gethostname()

# Get the local IP address
local_ip = socket.gethostbyname(hostname)

print(f"Local IP address: {local_ip}")
