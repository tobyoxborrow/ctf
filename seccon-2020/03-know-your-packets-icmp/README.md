# 03 Know your packets icmp

*PoNG*

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

Considering the challenge text, the response may be in an icmp echo reply.

Adding a wireshark filter:

```
icmp
```

This leaves 3554 packets. Most are Destination unreachable. We can filter it some more to just echo ping request and replies:

```
icmp.type == 8 or icmp.type == 0
```

This leaves 84 packets. I clicked through each one and found:

```
0000   e6 d9 08 26 f0 bd 5c 45 27 79 03 30 08 00 45 00   ...&..\E'y.0..E.
0010   00 54 22 f5 40 00 3a 01 2e 49 75 d3 5b f9 77 5f   .T".@.:..Iu.[.w_
0020   a6 3f 08 00 52 6b 27 39 00 02 7d f3 85 5b 00 00   .?..Rk'9..}..[..
0030   00 00 a0 37 0f 00 00 00 00 00 6c 61 67 7b 50 31   ...7......lag{P1
0040   4e 47 2e 50 6f 4e 47 7d 66 6c 61 67 7b 50 31 4e   NG.PoNG}flag{P1N
0050   47 2e 50 6f 4e 47 7d 66 6c 61 67 7b 50 31 4e 47   G.PoNG}flag{P1NG
0060   2e 50                                             .P
```

flag{P1NG.PoNG}
