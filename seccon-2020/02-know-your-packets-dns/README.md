# 02 Know your packets dns

Text me

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

Based on the challenge clue, perhaps the flag is in a DNS TXT record.

As this is a low point challenge, assumed traffic will be on the standard DNS port udp/53 (and maybe tcp/53).

Adding a wireshark filter, also trying for the word flag:

```
(udp.port == 53 and udp.payload ~ "flag") or (tcp.port == 53 and tcp.payload ~ "flag")
```

No results. Instead, just look for TXT packets, wireshark makes that simple:

```
dns.txt
```

1 packet.

```
0000   00 00 5e 00 01 64 e6 d9 08 26 f0 bd 08 00 45 00   ..^..d...&....E.
0010   00 c1 69 08 00 00 3f 11 22 b9 77 5f a6 3f 75 d3   ..i...?.".w_.?u.
0020   5b f9 00 35 b9 42 00 ad 39 e8 cf 87 85 00 00 01   [..5.B..9.......
0030   00 01 00 01 00 03 09 6c 6f 63 61 6c 68 6f 73 74   .......localhost
0040   00 00 10 00 01 c0 0c 00 10 00 01 00 09 3a 80 00   .............:..
0050   1d 1c 5a 6d 78 68 5a 33 74 69 59 54 56 6c 4e 6a   ..ZmxhZ3tiYTVlNj
0060   52 6b 49 47 5a 73 59 57 64 39 43 67 3d 3d c0 0c   RkIGZsYWd9Cg==..
0070   00 02 00 01 00 09 3a 80 00 02 c0 0c c0 0c 00 01   ......:.........
0080   00 01 00 09 3a 80 00 04 7f 00 00 01 c0 0c 00 1c   ....:...........
0090   00 01 00 09 3a 80 00 10 00 00 00 00 00 00 00 00   ....:...........
00a0   00 00 00 00 00 00 00 01 00 00 29 10 00 00 00 00   ..........).....
00b0   00 00 1c 00 0a 00 18 84 85 6b 5e d2 5d f6 d7 60   .........k^.]..`
00c0   3d 67 d1 5b 85 de e9 10 11 82 24 34 9b f4 3c      =g.[......$4..<
```

Decoded (left-pane), this is a TXT query for the name localhost. The reply
contains a 28 byte string value: ZmxhZ3tiYTVlNjRkIGZsYWd9Cg==

Looks like base64...

```Shell
~ echo 'ZmxhZ3tiYTVlNjRkIGZsYWd9Cg==' | base64 -d
flag{ba5e64d flag}
```
