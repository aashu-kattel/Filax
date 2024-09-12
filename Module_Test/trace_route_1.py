from lib2to3.fixes.fix_idioms import CMP
from telnetlib import IP
from scapy.all import *

def trace_route(destination):
    result = []
    for i in range(1, 30):
        pkt = IP(dst=destination, ttl=i) / CMP()
        reply = sr1(pkt, verbose=0, timeout=1)
        if reply is None:
            result.append(f"{i} * * * Request timed out.")
        elif reply.type == 0:
            result.append(f"{i} {reply.src} {reply.time:.3f} ms")
            break
        else:
            result.append(f"{i} {reply.src} {reply.time:.3f} ms")
    return result