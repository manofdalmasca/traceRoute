#!/usr/bin/env/ python3 
#to write a personalized traceroute program, meant to report on 
#the routes a packet takes to a given IP destination. This will be 
#accomplished by use of Echo Requests. See RFC 791 and RFC 792. 

import socket 
import time
import sys 

def outbound(shipment, endereco):
#python code for sending packets in general, involving sockets
#will take parameters for the destination and the content 
  outSock = socket.socket(
    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
  outSock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
  #necessary so that the kernel doesn't alter the header fields this program
  #will create, or so I'm told
  try: 
    outSock.sendto(shipment, (endereco, 0))
    outSock.close()
  #if for some reason a packet fails to even send properly, we shut down 
  except OSError as e: 
    print('Packet send failure') 
    outSock.close()
    exit(0)

#def inbound(patience): 
#python code for receiving packets in general, involving sockets 
#will take a timeout-value parameter, if it's not to wait forever
  inSock = socket.socket(
    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
  inSock.settimeout(patience)
  try: 
    [inCome, inAddr] = inSock.recvfrom(1024)
    inSock.close()
  except (OSError): 
    print('Packet receive failure') 
    inSock.close()
    exit(0) #if there's been a system error: we shut down 
  except (socket.timeout): 
  #on the other hand, a mere timeout can have any number of mundane causes
    inSock.close() #so we don't end the program outright
    return "***" #we only return a default value and move on 


#def makeIPHeader(): 
#code for building an IP header

#def makeICMPHeader(): 
#code for building an ICMP header

#def compilePacket(): 
#code for building the whole packet, complete with headers 

#def iterations(): 
#code for iteratively sending out packets with higher TTL's, and 
#receiving the responses 

#if __name__ == '__main__': 
#  iterations()
