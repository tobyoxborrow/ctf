# 09 Know your packets redis

Perhaps it's on another port

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Since these challenges use the same data, I had already found the flag for this
one as part of challenge 01. Using the following Wireshark filter, a few
different flags were visible:

```
tcp.payload ~ "flag{"
```

This appeared:

```
0000   00 00 5e 00 01 64 e6 d9 08 26 f0 bd 08 00 45 00   ..^..d...&....E.
0010   00 45 dc e2 40 00 3f 06 6f 65 77 5f a6 3f 75 d3   .E..@.?.oew_.?u.
0020   5b f9 7a 69 a5 56 b8 5d 09 06 9f f1 7a 9c 80 18   [.zi.V.]....z...
0030   00 e3 39 61 00 00 01 01 08 0a 64 fa d3 0f ad f1   ..9a......d.....
0040   5f c5 24 31 30 0d 0a 66 6c 61 67 7b 30 30 70 73   _.$10..flag{00ps
0050   7d 0d 0a                                          }..
```

Perhaps if we hadn't found it accidentally in the first challenge, we could
find out which port redis was using by first searching for the substring
"redis". Since it may appear in some system output, e.g. version number or
error message.

```
tcp.payload ~ "redis"
```

This finds 7 packets with some redis system messages. The server-side is using
port 31337. We can filter again just on that port:

```
tcp.port == 31337
```

This returns 556 packets. It's a lot to scroll through, but eventually we would
find the same flag.

flag{00ps}
