# 11 Know your packets redis-2

This may take some evaluation

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Based on the challenge text, I checked if there was any "eval" function for redis and there was. So I will assume it is something to do with that. Next filter by the redis port found in the 09 redis-1 challenge and the substring "eval".

```
tcp.port == 31337 and tcp.payload ~ "EVAL"
```

This found 36 packets.

The packets reveal someone trying out the eval function:

```
print "test"
return "test"
print string.lower("TEST")
print string.lower(test="TEST")
```

Eventually we come across:

```
0000   e6 d9 08 26 f0 bd 40 a6 77 42 b3 f0 08 00 45 00   ...&..@.wB....E.
0010   00 6a e8 5b 40 00 3a 06 68 c7 75 d3 5b f9 77 5f   .j.[@.:.h.u.[.w_
0020   a6 3f a8 b4 7a 69 5a b4 36 16 1a 83 8a b0 80 18   .?..ziZ.6.......
0030   01 ae b6 89 00 00 01 01 08 0a ae 0b 7c 2f 65 01   ............|/e.
0040   54 da 2a 33 0d 0a 24 34 0d 0a 65 76 61 6c 0d 0a   T.*3..$4..eval..
0050   24 32 36 0d 0a 66 6c 61 67 32 3d 22 46 6c 41 67   $26..flag2="FlAg
0060   7b 43 30 6d 50 6c 33 78 20 46 4c 41 47 7d 22 0d   {C0mPl3x FLAG}".
0070   0a 24 31 0d 0a 30 0d 0a                           .$1..0..
```

Following this a few attempts to make the string lowercase. So although it
wasn't shown in lowercase in the packets, it likely needs to be lowercase to
claim it.

flag{c0mpl3x flag}
