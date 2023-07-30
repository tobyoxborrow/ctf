# 12 Know your packets http-2

Hex is art!

# Design

Uses the common 500MB dump.pcap (of approximately 880,000 packets) used for all the "Know your packets" challenges.

# Write-up
Loaded up the file into Wireshark.

There is not much traffic on port 80 so instead I used the filter:

```
http
```

I found an interesting packet while investigating the first HTTP challenge. It
appears many times in multiple packets so is easy to find.

The server responds to a "GET /" request with the HTML:

```html
<html><body><h1>obfuscated flag:</h1><b>
0000000 2020 5f5f 5f20 2020 2020 2020 2020 2020
0000010 2020 2020 5f20 5f5f 2020 205f 5f20 5f5f
0000020 205f 2020 2020 2020 205f 205f 2020 205f
0000030 5f20 2020 2020 2020 5f20 5f5f 5f5f 5f5f
0000040 2020 0a20 2f20 5f20 207c 207c 5f5f 5f20
0000050 2020 5f5f 5f20 2020 202f 202f 7c7c 7c20
0000060 207c 5f5f 7c5f 2020 5f5f 2f5f 2f20 7c20
0000070 7c20 7c20 207c 207c 5f20 5f20 5f7c 5f5f
0000080 2020 205c 205c 0a20 207c 5f7c 207c 2f7c
0000090 5f20 2060 2f7c 5f20 2060 7c7c 7c20 207c
00000a0 7c7c 7c20 5f7c 5f5f 5c20 2f20 5f20 7c5f
00000b0 7c20 7c20 7c20 7c20 207c 5f7c 207c 5f27
00000c0 7c5f 2f20 2f20 7c20 7c20 0a20 207c 5f20
00000d0 207c 207c 5f28 207c 207c 5f28 207c 203c
00000e0 203c 5f7c 205f 2020 7c5f 5f5f 2029 207c
00000f0 5f28 7c5f 7c20 7c20 7c20 5f5f 2020 5f20
0000100 207c 207c 2020 202f 202f 2020 203e 0a3e
0000110 5f7c 207c 5f7c 5c7c 5f5f 5f2c 5c7c 5f5f
0000120 202c 7c7c 7c20 2020 7c20 7c5f 5f7c 5f5f
0000130 2f5f 5c20 5f5f 7c5f 7c5f 7c5f 2020 2020
0000140 5f7c 207c 5f7c 207c 2f20 2f5f 2020 7c20
0000150 7c20 0a20 2020 2020 2020 2020 2020 2020
0000160 7c20 5f5f 2f5f 2020 5f5c 205c 2020 2020
0000170 2020 2020 2020 2020 2020 2020 2020 2020
*
0000190 2020 5f2f 202f 0a20
0000198
</b></html>
````

Which looks like a hexdump of binary data...

The man page for hexdump doesn't indicate it can reverse. However, xxd's says:
"xxd creates a hex dump of a given file or standard input.  It can also convert
a hex dump back to its original binary form."

```Shell
% xxd -r hex_input.txt > hex_output
% file !$
file hex_output
hex_output: data
```

The file is actually some ASCII art:

```text
  ___               _ __   __ __ _       _ _   __       _ ______
 / _  | |___   ___    / /|||  |__|_  __/_/ | | |  | |_ _ _|__   \ \
  |_| |/|_  `/|_  `|||  |||| _|__\ / _ |_| | | |  |_| |_'|_/ / | |
  |_  | |_( | |_( | < <_| _  |___ ) |_(|_| | | __  _  | |   / /   >
>_| |_|\|___,\|__ ,|||   | |__|__/_\ __|_|_|_    _| |_| |/ /_  | |
             | __/_  _\ \                      _/ /
```

I can kind of make out "flag{", but isn't quite laid out right or the spaces are purposefully wrong.

I've use the figlet command a lot for creating ASCII art in server banners, so
the general style looked familiar.  I used figlet with various fonts and found
it was using the "standard" font. Using that I have some reference of what it
*should* look like.

```text
  __ _               __
 / _| | __ _  __ _  / /
| |_| |/ _` |/ _` || |
|  _| | (_| | (_| < <
|_| |_|\__,_|\__, || |
             |___/  \_\
```

Using this I can see every character has been swapped with its neighbour. This
may be byte ordering. little vs big endian. xxd doesn't seem to automatically
convert with its revert option.

Rather than find the right option I wrote a python script to swap the chars.

```Shell
% ./transpose.py
  ___               _ __   __ __ _       _ _   __       _ ______
 / _  | |___   ___    / /|||  |__|_  __/_/ | | |  | |_ _ _|__   \ \
  |_| |/|_  `/|_  `|||  |||| _|__\ / _ |_| | | |  |_| |_'|_/ / | |
  |_  | |_( | |_( | < <_| _  |___ ) |_(|_| | | __  _  | |   / /   >
>_| |_|\|___,\|__ ,|||   | |__|__/_\ __|_|_|_    _| |_| |/ /_  | |
             | __/_  _\ \                      _/ /


  __ _               ___  _  ____       _ _   _  _       _______
 / _| | __ _  __ _  / / || || ___|  ___/ / | | || |  _ _|___  \ \
| |_| |/ _` |/ _` || || || ||___ \ / __| | | | || |_| '__| / / | |
|  _| | (_| | (_| < < |__   _|__) | (__| | | |__   _| |   / /   > >
|_| |_|\__,_|\__, || |   |_||____/ \___|_|_|    |_| |_|  /_/   | |
             |___/  \_\                                       /_/
```

This is clearly a flag, but it wasn't asccepted.

Just to make sure I wasn't misunderstanding one of the characters due to the
ASCII art I used figlet one what I thought I read, and it outputs the same:

```Shell
% figlet "flag{45c114r7}"
  __ _               ___  _  ____       _ _ _  _       _______
 / _| | __ _  __ _  / / || || ___|  ___/ / | || |  _ _|___  \ \
| |_| |/ _` |/ _` || || || ||___ \ / __| | | || |_| '__| / / | |
|  _| | (_| | (_| < < |__   _|__) | (__| | |__   _| |   / /   > >
|_| |_|\__,_|\__, || |   |_||____/ \___|_|_|  |_| |_|  /_/   | |
             |___/  \_\                                     /_/
```

That's when I noticed there should be a space between the 4 and r.

45c11 4r7 == ASCII ART

flag{45c11 4r7}
