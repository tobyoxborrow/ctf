# 04 Know your packets mysql

Another crack me?

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard MySQL port 3306.

```
tcp.port == 3306
```

This resulted in 270 packets.

Reading some of the streams I could see a "shadow" table being created with
username and password columns.

I tweaked the filter to look for packets related to the shadow table:

```
tcp.port == 3306 && tcp.payload ~ "shadow"
```

This resulted in about 22 packets.

I could see the table was created, populated with data loaded from the file
/etc/shadow, then a select * from shadow where username='mysqlflag'.

```
0000   e6 d9 08 26 f0 bd 5c 45 27 79 03 30 08 00 45 08   ...&..\E'y.0..E.
0010   00 68 c1 43 40 00 3a 06 8f d9 75 d3 5b f9 77 5f   .h.C@.:...u.[.w_
0020   a6 3f a2 32 0c ea 19 9f 7e 98 ca d1 1e 31 80 18   .?.2....~....1..
0030   03 c9 1c 6f 00 00 01 01 08 0a ae 2f 54 28 65 09   ...o......./T(e.
0040   a1 b4 30 00 00 00 03 73 65 6c 65 63 74 20 2a 20   ..0....select *
0050   66 72 6f 6d 20 73 68 61 64 6f 77 20 77 68 65 72   from shadow wher
0060   65 20 75 73 65 72 6e 61 6d 65 3d 27 6d 79 73 71   e username='mysq
0070   6c 66 6c 61 67 27                                 lflag'
```

Due to the wireshark filters the response was not in the filtered output, so
right-click Follow -> TCP Stream and found.

Within that I found the response to the query:

```
[snip]
0230   76 69 74 79 61 67 65 0c 08 00 0a 00 00 00 fd 00   vityage.........
0240   00 00 00 00 05 00 00 0b fe 00 00 22 00 80 00 00   ..........."....
0250   0c 09 6d 79 73 71 6c 66 6c 61 67 62 24 36 24 32   ..mysqlflagb$6$2
0260   37 44 66 6c 4d 2e 4e 24 68 73 52 58 77 64 33 57   7DflM.N$hsRXwd3W
0270   55 4c 54 49 76 36 54 68 6b 43 42 6c 32 6d 49 53   ULTIv6ThkCBl2mIS
0280   49 49 72 6a 69 31 79 57 43 63 33 44 47 79 56 4a   IIrji1yWCc3DGyVJ
0290   4d 72 54 68 66 63 6a 45 50 64 7a 56 2e 79 54 66   MrThfcjEPdzV.yTf
02a0   74 32 4a 6e 46 42 36 44 64 52 67 77 77 36 69 6f   t2JnFB6DdRgww6io
02b0   45 63 46 4a 4a 52 61 57 4d 57 61 70 31 2f 05 31   EcFJJRaWMWap1/.1
02c0   37 37 37 32 01 30 05 39 39 39 39 39 01 37 00 00   7772.0.99999.7..
02d0   00 05 00 00 0d fe 00 00 22 00                     ........".
```

There's clearly a hash in there but it needs a bit of cleanup to extract it
exactly without pulling in extra characters which would kill any chances of
cracking it.

Wireshark helpfully decodes the packet and you can copy the specific text value
from the left-pane without having to mess with the hex.

```
$6$27DflM.N$hsRXwd3WULTIv6ThkCBl2mISIIrji1yWCc3DGyVJMrThfcjEPdzV.yTft2JnFB6DdRgww6ioEcFJJRaWMWap1/
```

And lookup what kind of hash this may be...

```Shell
$ hashid
$6$27DflM.N$hsRXwd3WULTIv6ThkCBl2mISIIrji1yWCc3DGyVJMrThfcjEPdzV.yTft2JnFB6DdRgww6ioEcFJJRaWMWap1/
Analyzing '$6$27DflM.N$hsRXwd3WULTIv6ThkCBl2mISIIrji1yWCc3DGyVJMrThfcjEPdzV.yTft2JnFB6DdRgww6ioEcFJJRaWMWap1/'
[+] SHA-512 Crypt
```

The challenge text implies something to crack, but this seems like a lot of
work for the number of points available (lowest in the game).

That's as far a I got originally in 2020. As I'm writing the other challenges up, I decided to revisit it...

Initially I thought perhaps the hash might be common and tried it on some
online hash "cracking" sites, but they didn't like the format. I'm going to
have to crack it the traditional way...

I created a dummy shadow file for John by taking an entry from a real /etc/shadow and replacing the username and hash.

```Shell
cat shadow
mysqlflag:$6$27DflM.N$hsRXwd3WULTIv6ThkCBl2mISIIrji1yWCc3DGyVJMrThfcjEPdzV.yTft2JnFB6DdRgww6ioEcFJJRaWMWap1/:19293:0:99999:7:::
```

Try John with the defaults, since this is a low point challenge, this may be enough:

```Shell
~/github.com/JohnTheRipper/run/john shadow
```

After a few hours that didn't find anything. Since the flag is probably in the
format flag{}, this isn't unexpected.

Next I created a wordlist rule for John to wrap up words in "flag{}":

```Shell
$ cat john-local.conf
[List.Rules:flag]
A0"flag{"Az"}"
```

Then used that with a few basic wordlists:

```Shell
./github.com/JohnTheRipper/run/john --wordlist:/usr/share/dict/words --rules:flag shadow
./github.com/JohnTheRipper/run/john --wordlist:~/github.com/SecLists/PasswordLists/rockyou.txt --rules:flag shadow
```

Still nothing. Almost giving up, I ran cewl against the mysql wikipedia article
to create a mysql themed wordlist:

```Shell
cewl https://en.wikipedia.org/wiki/MySQL --depth 1 --write mysql.txt
```

And use that with John, success:

```Shell
./github.com/JohnTheRipper/run/john --wordlist:mysql.txt --rules:flag shadow
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Warning: OpenMP is disabled; a non-OpenMP build may be faster
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
Enabling duplicate candidate password suppressor
0g 0:00:00:06 27.12% (ETA: 15:29:23) 0g/s 1768p/s 1768c/s 1768C/s flag{extension}..flag{factbookrft}
flag{mysql}      (mysqlflag)
1g 0:00:00:13 DONE (2023-07-29 15:29) 0g/s 1764p/s 1764c/s 1764C/s flag{muna}..flag{mythology}
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

flag{mysql}
