# 13 Know your packets ftp-2

Extract the file

# Design

Uses the common 500MB dump.pcap (of approximately 880,000 packets) used for all the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard FTP ports 20 and 21.

```
tcp.port == 20 or tcp.port == 21
```

This leaves 468 packets.

From the hint text we probably should look for file transfers, maybe even binary files.

While scrolling, by chance I saw some file transfers for flag.gif. I assume the
image shows the flag text if we can download and view it.

The file data wasn't in my wireshark filtered packets though, so I would need to change my filters.

FTP uses a command and data channels on different ports, the passive command was issued with a high number port:

This was easily visible in Wireshark's decoded data (middle) pane: Passive port: 64744

So add that to the wireshark filter:

```
tcp.port == 20 or tcp.port == 21 or tcp.port == 64744
```

Once I found the right stream, right-click -> Follow -> TCP Stream

Select "Raw" for "Show and save data as"

On the resulting window save the as "flag.gif".

The image itself was some kind of flag but I didn't recognise it and there was no text.

Though within the file data was hidden text that was easy to find...

```bash
% strings flag.gif | less
[snip]
synt{1z gree1o1r j17u 7ur t1zc}
```

I assume it is rot13...

```
% echo 'synt{1z gree1o1r j17u 7ur t1zc}' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
flag{1m terr1b1e w17h 7he g1mp}
```
