# 01 Know your packets telnet

What a lovely environment.

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard telnet port 23.

```
tcp.port == 23
```

I just scrolled through the data packets until I came across:

```
0000   e6 d9 08 26 f0 bd 5c 45 27 79 03 30 08 00 45 10   ...&..\E'y.0..E.
0010   00 7f fc 61 40 00 3a 06 54 9c 75 d3 5b f9 77 5f   ...a@.:.T.u.[.w_
0020   a6 3f a7 8a 00 17 b8 88 38 99 c7 51 58 40 80 18   .?......8..QX@..
0030   00 e5 24 69 00 00 01 01 08 0a ad d1 33 b7 64 f2   ..$i........3.d.
0040   c8 09 ff fa 20 00 33 38 34 30 30 2c 33 38 34 30   .... .38400,3840
0050   30 ff f0 ff fa 27 00 03 66 6c 61 67 01 7b 67 61   0....'..flag.{ga
0060   6c 66 20 64 65 73 72 65 76 65 72 7d 67 61 6c 66   lf desrever}galf
0070   ff f0 ff fa 18 00 73 63 72 65 65 6e 2e 78 74 65   ......screen.xte
0080   72 6d 2d 32 35 36 63 6f 6c 6f 72 ff f0            rm-256color..
```

flag{galf desrever}

Which didn't work as-is, but looking more closely it needed a little transformation:

flag{reversed flag}

The following wireshark filter would have found it more quickly:

```
tcp.port == 23 and tcp.payload ~ "flag"
```
