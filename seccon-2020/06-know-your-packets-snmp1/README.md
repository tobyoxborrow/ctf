# 01 Know your packets snmp-1

In the community.

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard SMTP port:

```
udp.port == 161
```

Very early on, and in pretty much every packet, we can see the flag:

```
0000   e6 d9 08 26 f0 bd 5c 45 27 79 03 30 08 00 45 00   ...&..\E'y.0..E.
0010   00 4a c7 4f 40 00 3a 11 89 e8 75 d3 5b f9 77 5f   .J.O@.:...u.[.w_
0020   a6 3f c4 16 00 a1 00 36 d3 0c 30 2c 02 01 00 04   .?.....6..0,....
0030   0c 66 6c 61 67 7b 70 75 62 6c 21 63 7d a1 19 02   .flag{publ!c}...
0040   04 33 ac 2c 01 02 01 00 02 01 00 30 0b 30 09 06   .3.,.......0.0..
0050   05 2b 06 01 02 01 05 00                           .+......
```

flag{publ!c}
