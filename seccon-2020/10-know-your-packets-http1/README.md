# 10 Know your packets http-1

It's really rather basic :P

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

There is not much traffic on port 80 so instead I used the filter:

```
http
```

1101 packets.

Based on the clue I'm assuming the flag is in a HTTP Basic Auth header, so adjust the filter:

```
http and http.authbasic
```

11 packets.

There are two packets with the auth header:

```
0000   41 75 74 68 6f 72 69 7a 61 74 69 6f 6e 3a 20 42   Authorization: B
0010   61 73 69 63 20 63 32 78 31 5a 33 4d 36 61 32 6c   asic c2x1Z3M6a2l
0020   6a 61 32 46 7a 63 77 3d 3d 0d 0a                  ja2Fzcw==..
```

Which decodes to: slugs:kickass

(Wireshark will decode it for you in the middle pane)

And:

```
0290   72 4b 30 0d 0a 41 75 74 68 6f 72 69 7a 61 74 69   rK0..Authorizati
02a0   6f 6e 3a 20 42 61 73 69 63 20 64 58 4e 6c 63 6a   on: Basic dXNlcj
02b0   70 4e 57 6c 64 48 51 31 6f 7a 4d 30 35 57 4d 6c   pNWldHQ1ozM05WMl
02c0   64 5a 54 6c 70 53 52 55 4a 54 56 7a 52 5a 57 6c   dZTlpSRUJTVzRZWl
02d0   46 4e 55 6c 4e 59 4d 6b 4e 52 50 51 3d 3d 0d 0a   FNUlNYMkNRPQ==..
```

Which decodes to: user:MZWGCZ33NV2WYNZREBSW4YZQMRSX2CQ=

The = on the end makes it look like base64 encoded data, but that didn't decode:

```Shell
$ echo 'MZWGCZ33NV2WYNZREBSW4YZQMRSX2CQ=' | base64 -d
1��	��5]�`�Q��P1��
```

But turned out to be base32 encoded instead:

```Shell
$ echo 'MZWGCZ33NV2WYNZREBSW4YZQMRSX2CQ=' | base32 -d
flag{mul71 enc0de}
```
