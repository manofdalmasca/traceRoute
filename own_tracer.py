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


def makeIPHeader(slouchTowards, slouchFrom, slouchID, expirationDate): 
#code for building an IP header, to be returned in the form of packed 
#binary data 
  #For IPv4 and a 5-word header: '0100' + '0101' = '01000101' = 69
  versionAndIHL = 69 
  serviceType = 0 #we don't need precedence or extra throughput, and 
  #we'll be implementing our own form of reliability. What's more, there's 
  #no guarantee that the en-route networks will even do anything special 
  #if these things are requested. So as not to request them, we'll 
  #leave [serviceType] as 0 (see RFC 791). 
  totalLength = 28 #in terms of bytes: 20 for the IP header, 8 for the ICMP 
  #header, and nothing after that (at least not for outbound packets).
  #and we'll get a unique ID from the calling context, as [slouchID]. 
  flags_n_frags = 0 #may_fragment, is_last_fragment, and is_first_fragment
  #all understood from the mere number 0, as per RFC 791 
  #we also get a time to live from the calling context, as [expirationDate]. 
  protocolVal = 1 #for ICMP, as per RFCs 791 and 792 
  checkSum = 0 #not what the final checksum will be, but with any luck, 
  #that won't be our problem 
  #and we get our source and destination from the calling context 

  #The following section will build (most of) the bitstring representing 
  #our IP header. See the documentation for Python's [struct] module for 
  #an explanation of what follows. 
  ip_header = struct.pack('!BBHHHBBH', 
  versionAndIHL, 
  serviceType, 
  totalLength, 
  slouchID, 
  flags_n_frags, 
  expirationDate, 
  protocolVal, 
  checkSum) 

  #It remains to tack on the source and destination variables, which 
  #will be given in a slightly different format than the other header fields
  #(which is why we can't just [struct.pack] them). The useful part is that 
  #bitstrings can be concatenated just like regular strings, at least in 
  #python. 
  ip_header = ip_header + socket.inet_aton(slouchFrom) #source 
  ip_header = ip_header + socket.inet_aton(slouchTowards) #destination 
  #and we are done 
  return ip_header
   


#def makeICMPHeader(controlID, sequenceCount): 
#code for building an ICMP header
  typeVal = 8 #for an Echo Request, as per RFC 792 
  codeVal = 0 #irrelevant in this context; set to 0 as per RFC 792 
  checker = 0 #to begin with, anyway 
  #and the calling context gives us an ID number for this ICMP call 
  #as well as a sequence number 

  #What follows will build the bitstring representing our ICMP header. 
  #See the Python documentation on [struct.pack] for an explanation of what 
  #follows. 
  icmp_header = struct.pack('!BBHHH', 
  typeVal, 
  codeVal, 
  checker, 
  controlID, 
  sequenceCount) 

  return icmp_header 
  

#def compilePacket(): 
#code for building the whole packet, complete with headers 

#def iterations(): 
#code for iteratively sending out packets with higher TTL's, and 
#receiving the responses 

#if __name__ == '__main__': 
#  iterations()
