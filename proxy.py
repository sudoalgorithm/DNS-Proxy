"""
Python Libraies important
Socket: To create socket object
SSL: To facilate the TLS connection
OS: Interact with the underlying os to get environment variables
logging: to log message
binascii: convert binary to Hexadecimal conversion
"""
import socket, ssl, sys, binascii, os, logging

"""
Function Name: tcp_listenere
Arguments:
1. host -> address of the source host-> string
2. port -> 53 because we want to listen on port 53 -> int
Objective: To create a socket which listens on port 53
"""

def tcp_listenere(source_host, source_port):
  port = int(source_port)
  host = str(source_host)
  dns_server = 'dns.google'
  dns_port = 853
  try:
    print("Proxy is starting on host {} and port {}".format(host, port))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    tcp_socket.listen(5)
    while True:
      conn, addr = tcp_socket.accept()
      data = conn.recv(1024)
      result = request_handler(data, dns_server, dns_port)
      conn.sendto(result, addr)
  except Exception as connection_exception:
    print(str(connection_exception))
    tcp_socket.close()

"""
Function Name: connection_to_dns_server
Arguments:
1. dns_host -> address of the destination dns server -> string
2. dns_port -> port of the destination dns server -> int
Objective: To create tcp connection with DNS Server over TLS
Working: 
1. Using the socket standard liberay in python we create a socket to setup a connection with our destination Google's DNS Server on host dns.google and port 853 using self-signed certificate
2. SOCK_STREAM because it the standard socket type for TCP
3. wrap_socket method is used to tip with the connection with ssl context
"""
def connection_to_dns_server(dns_host, dns_port):
  print('connection to dns initiated dns server')
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=dns_host)
  wrappedSocket.connect((dns_host , dns_port))
  return wrappedSocket

"""
Function Name: send_query
Arguments:
1. connection_socket -> socket object created to communicate with DNS Server
2. data -> data 
Objective: to get the data from the tcp client and close the socket from where data is being received.
"""
def send_query(connection_socket,data):
  connection_socket.send(data)
  recevied_data=connection_socket.recv(1024)
  connection_socket.close()
  return recevied_data

"""
Function Name: request_handler
Arguments:
1. data -> socket object created to communicate with DNS Server
1. dns_host -> address of the destination dns server -> string
2. dns_port -> port of the destination dns server -> int
Objective: Helper function to handle the communication between destination dns server and data recevied from the client.
           Also help in the conversion of the data recevied from the destination dns server.
"""

def request_handler(data,dns_host,dns_port):
  print("Sending request to the DNS Server")
  tls_conn_sock=connection_to_dns_server(dns_host,dns_port) 
  tcp_result = send_query(tls_conn_sock, data)
  if tcp_result:
    # Get first 6 bytes from response
    rcode = tcp_result[:6].hex()
    # Get 12th bit from the response
    rcode = str(rcode)[11:]
    if (rcode != '0'):
      sys.exit('Error RCODE', rcode)
    else:
      return tcp_result
  else:
    sys.exit('Error occurred')

if __name__ == '__main__':
  tcp_listenere('0.0.0.0','53')
  