# 01 Know your packets snmp-2

Where are we located?

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard SMTP port:

```
udp.port == 161
```

This produces 4870 packets. The bulk of the output is an snmpwalk like dump from the service.

I sorted the packets by length and reviewed the longest ones, as most of the packets are numerical responses and small and can be skipped.

Sure enough after not too long I can find:

```
0000   00 00 5e 00 01 64 e6 d9 08 26 f0 bd 08 00 45 00   ..^..d...&....E.
0010   00 71 94 e1 40 00 3f 11 b7 2f 77 5f a6 3f 75 d3   .q..@.?../w_.?u.
0020   5b f9 00 a1 aa 4b 00 5d 39 98 30 53 02 01 00 04   [....K.]9.0S....
0030   0c 66 6c 61 67 7b 70 75 62 6c 69 63 7d a2 40 02   .flag{public}.@.
0040   04 54 af a5 9b 02 01 00 02 01 00 30 32 30 30 06   .T.........0200.
0050   08 2b 06 01 02 01 01 06 00 04 24 66 6c 61 67 7b   .+........$flag{
0060   53 69 74 74 69 6e 67 20 6f 6e 20 74 68 65 20 44   Sitting on the D
0070   6f 63 6b 20 6f 66 20 74 68 65 20 42 61 79 7d      ock of the Bay}
```

flag{Sitting on the Dock of the Bay}
