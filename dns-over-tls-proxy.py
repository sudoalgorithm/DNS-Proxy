import socket, ssl, sys, binascii, os, logging
import ssl
import sys
import binascii
import os

# 
def send_query(tls_conn_sock,dns_query):
  tls_conn_sock.send(dns_query)
  result=tls_conn_sock.recv(1024)
  tls_conn_sock.close()
  return result

# TLS connection with upstream dns server  
def tls_connection(dns,port):
  #print('connection to dns initiated', dns, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=dns)
  wrappedSocket.connect((dns , int(port)))
  #print('wrapped socket created')
  return wrappedSocket

# pretty format hex string
def format_hex(hex):
  octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
  pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
  return "\n".join(pairs)

# send new request to upstream dns server and return the result
def new_request(data,address,dns,port):
  #print ('new thread running')
  tls_conn_sock=tls_connection(dns,port) 
  tcp_result = send_query(tls_conn_sock, data)
  if tcp_result:
    # Get first 6 bytes from response
    rcode = tcp_result[:6].encode("hex")
    # Get 12th bit from the response
    rcode = str(rcode)[11:]
    if (rcode != '0'):
      sys.exit('Error RCODE', rcode)
    else:
      return tcp_result
  else:
    sys.exit('Error occurred')

if __name__ == '__main__':
  port = 53
  host='0.0.0.0'
  dns_server = os.environ['DNS_SERVER']
  dns_port   = os.environ['DNS_PORT']
  #print (dns_server)

  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    while True:
      conn, addr = s.accept()
      data = conn.recv(1024)
      result = new_request(data, addr, dns_server, dns_port)
      #print('result is ', result.encode("hex"))
      #conn.sendall(result)
      conn.sendto(result, addr)
  except:
    #print (e)
    s.close()