# 01 Know your packets ftp-1

Did we mention this was an *insecure* protocol?

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard FTP ports 20 and 21.

Adding a wireshark filter:

```
tcp.port == 20 or tcp.port == 21
```

This leaves 468 packets.

I assumed the file would be seen as a ASCII file transfer, so skimmed through
the packets looking for file transfers. But as I did that I spotted the flag in
the clear as the password:

```
0000   e6 d9 08 26 f0 bd 5c 45 27 79 03 30 08 00 45 10   ...&..\E'y.0..E.
0010   00 49 52 7d 40 00 3a 06 fe b6 75 d3 5b f9 77 5f   .IR}@.:...u.[.w_
0020   a6 3f af 4e 00 15 5b 6b 75 80 dc de dd b1 80 18   .?.N..[ku.......
0030   00 e5 f8 ae 00 00 01 01 08 0a ac 8a bc 3c 64 a1   .............<d.
0040   2a 29 50 41 53 53 20 66 6c 61 67 7b 31 6e 35 33   *)PASS flag{1n53
0050   63 75 72 33 7d 0d 0a                              cur3}..
```

A quicker method would have been:

```
tcp.payload ~ "flag{"
```

And since the dump.pcap is shared by multiple challenges this found two more flags...

```
0000   00 00 5e 00 01 64 e6 d9 08 26 f0 bd 08 00 45 00   ..^..d...&....E.
0010   00 45 dc e2 40 00 3f 06 6f 65 77 5f a6 3f 75 d3   .E..@.?.oew_.?u.
0020   5b f9 7a 69 a5 56 b8 5d 09 06 9f f1 7a 9c 80 18   [.zi.V.]....z...
0030   00 e3 39 61 00 00 01 01 08 0a 64 fa d3 0f ad f1   ..9a......d.....
0040   5f c5 24 31 30 0d 0a 66 6c 61 67 7b 30 30 70 73   _.$10..flag{00ps
0050   7d 0d 0a                                          }..
```

(that one turned out to be the flag for redis1)

And:

```
0000   e6 d9 08 26 f0 bd 40 a6 77 42 b3 f0 08 00 45 00   ...&..@.wB....E.
0010   00 65 43 e9 40 00 3a 06 0d 3f 75 d3 5b f9 77 5f   .eC.@.:..?u.[.w_
0020   a6 3f a5 c4 7a 69 f0 b2 9c 6b 16 8f cc a8 80 18   .?..zi...k......
0030   00 e5 07 a1 00 00 01 01 08 0a ae 03 3d d9 64 ff   ............=.d.
0040   45 59 2a 33 0d 0a 24 33 0d 0a 73 65 74 0d 0a 24   EY*3..$3..set..$
0050   35 0d 0a 66 6c 61 67 32 0d 0a 24 31 38 0d 0a 46   5..flag2..$18..F
0060   6c 41 67 7b 43 30 6d 50 6c 33 78 20 46 4c 41 47   lAg{C0mPl3x FLAG
0070   7d 0d 0a                                          }..
```

For this challenge though, the flag was the first of the three I found:

flag{1n53cur3}
