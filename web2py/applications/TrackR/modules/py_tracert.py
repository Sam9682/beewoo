#!/usr/bin/python

import socket
import struct
import sys


global lst_IPs
lst_IPs = []

def TraceRoutelistIpAddresses(dest_name):
    #dest_addr = socket.gethostbyname(dest_name)
    lst_IPs = []
    dest_addr = dest_name
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)

        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

        recv_socket.bind(("", port))
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 3
        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as (errno, errmsg):
                tries = tries - 1

        send_socket.close()
        recv_socket.close()

        if not finished:
            pass

        if curr_addr is not None:
            lst_IPs.append(curr_addr)
        else:
            curr_host = ""

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
    		return lst_IPs
    return lst_IPs

if __name__ == "__main__":
	if len(sys.argv) > 1:
		the_ip = sys.argv[1]
	else:
		the_ip = '8.8.8.8'
	
	lst_IPs = TraceRoutelistIpAddresses(the_ip)
	for i in range(1,len(lst_IPs)):
	       	print("%s\n" % (lst_IPs[i]))
