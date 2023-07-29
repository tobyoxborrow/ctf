# 08 Know your packets dns-2

Bad guys often tunnel their way out of the network

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

Based on the challenge clue, perhaps the flag is hidden in some "DNS
tunnelling" traffic, so I need to find some non-standard DNS traffic.

Start by just looking at all DNS traffic:

```
dns
```

This found 331 packets.

I looked up DNS tunneling to see if there were any patterns to look for. One
might be traffic to a specific domain that is acting as the tunnel. So I sorted
the packets by size looking for a series of large requests, but there were
none. Another indicator of DNS tunneling would be lots of requests to the same
domain. There was some standard stuff, but then I found a lot of TXT requests
for domains with tunnel in their name. This seemed close, but they were all
trying different names and failing to resolve. I kept looking up and down.

Then I saw it, looking at the packets in Wireshark in order, they spelled out the flag:

```
No.	Time	Source	Destination	Protocol	Length	Info
533841  7551.215355 117.211.91.249  119.95.166.63   DNS 101 Standard query 0x01b6 TXT f.tunnel.localhost OPT
533842	7551.215671	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x01b6 No such name TXT f.tunnel.localhost SOA localhost OPT
533845	7551.243036	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x8d7b TXT l.tunnel.localhost OPT
533846	7551.243293	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x8d7b No such name TXT l.tunnel.localhost SOA localhost OPT
533847	7551.276323	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x8920 TXT a.tunnel.localhost OPT
533848	7551.276599	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x8920 No such name TXT a.tunnel.localhost SOA localhost OPT
533849	7551.306700	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xd831 TXT g.tunnel.localhost OPT
533850	7551.306981	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xd831 No such name TXT g.tunnel.localhost SOA localhost OPT
533851	7551.335347	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xf945 TXT {.tunnel.localhost OPT
533852	7551.335658	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xf945 No such name TXT {.tunnel.localhost SOA localhost OPT
533853	7551.368351	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x46b9 TXT t.tunnel.localhost OPT
533854	7551.368648	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x46b9 No such name TXT t.tunnel.localhost SOA localhost OPT
533855	7551.402361	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xd9cd TXT u.tunnel.localhost OPT
533856	7551.402678	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xd9cd No such name TXT u.tunnel.localhost SOA localhost OPT
533857	7551.433299	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x61e4 TXT n.tunnel.localhost OPT
533858	7551.433621	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x61e4 No such name TXT n.tunnel.localhost SOA localhost OPT
533859	7551.459454	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x568e TXT n.tunnel.localhost OPT
533860	7551.459779	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x568e No such name TXT n.tunnel.localhost SOA localhost OPT
533861	7551.486355	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x29bd TXT e.tunnel.localhost OPT
533862	7551.486612	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x29bd No such name TXT e.tunnel.localhost SOA localhost OPT
533863	7551.515334	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x630e TXT l.tunnel.localhost OPT
533864	7551.515606	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x630e No such name TXT l.tunnel.localhost SOA localhost OPT
533865	7551.541311	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x76df TXT m.tunnel.localhost OPT
533866	7551.541581	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x76df No such name TXT m.tunnel.localhost SOA localhost OPT
533867	7551.568372	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x5ba0 TXT e.tunnel.localhost OPT
533868	7551.568571	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x5ba0 No such name TXT e.tunnel.localhost SOA localhost OPT
533869	7551.596398	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xc78c TXT o.tunnel.localhost OPT
533870	7551.596616	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xc78c No such name TXT o.tunnel.localhost SOA localhost OPT
533871	7551.625317	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xb887 TXT u.tunnel.localhost OPT
533872	7551.625477	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xb887 No such name TXT u.tunnel.localhost SOA localhost OPT
533873	7551.652398	117.211.91.249	119.95.166.63	DNS	101	Standard query 0xc5e2 TXT t.tunnel.localhost OPT
533874	7551.652666	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0xc5e2 No such name TXT t.tunnel.localhost SOA localhost OPT
533875	7551.680476	117.211.91.249	119.95.166.63	DNS	101	Standard query 0x64d4 TXT }.tunnel.localhost OPT
533876	7551.680681	119.95.166.63	117.211.91.249	DNS	158	Standard query response 0x64d4 No such name TXT }.tunnel.localhost SOA localhost OPT
```

flag{tunnelmeout}
