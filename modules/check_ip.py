# Check if address is valid IP or NOT
# Will return False if entered IP is not a Valid IP.

import socket

def ip_address_is_valid(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        return False
    else:
        return True