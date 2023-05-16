# 07 Two For One

I've set up my first service! I hope I did it all correctly...

## Design

The challenge includes a website and an SSH service.

The website displaying the text "Check out my logo" and a single image.

## Write-up

The HTML of the page is very minimal and provides just enough for the text and image.

```HTML
1 <htm1>
2 <head>
3 <title>Two for one‹/title>
4 </head>
5 <body>
6 <!-- old data -->
7 <h1>Check out my logo:</h1>
8 <img src=" /imgs/logo.png" />
9 </body>
10 </html>
```

The image is stored in an /imgs directory, browsing to that reveals another file called selfie.jpg.

In selfie.jpg is a picture of someone standing infront of a whiteboard. On the whiteboard is the text:

```Text
User: doubledipper
Pass: <obscured>
```

The actual password is not visible due to the person in the photo.

I tried some investigation into the selfie.jpg itself to see if it provided any more hints in the image data itself. This was ultimately fruitless and not necessary, included for reference.

Checking the file with binwalk found some TIFF data. This felt like there could be another image hidden with the first. However, in retrospect this is probably a thumbnail of the main image and not part of the challenge.

```Bash
root@kali# binwalk selfie.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
30            0x1E            TIFF image data, big-endian, offset of first image directory: 8
```

EXIF data may reveal some clues...

```Bash
root@kali# exiv2 selfie.jpg
File name       : selfie.jpg
File size       : 58086 Bytes
MIME type       : image/jpeg
Image size      : 432 x 576
Camera make     : Apple
Camera model    : iPhone 6
Image timestamp : 2019:08:23 09:57:36
Image number    :
Exposure time   : 1/30 s
Aperture        : F2.2
Exposure bias   : 0 EV
Flash           : No flash function
```

At this point I suspected perhaps this was a legitimate data segment and not part of the challenge. Since the image mentioned iPhone 6, I went to flickr to look for other images by this camera and in particular the selfie front-facing camera: https://www.flickr.com/search/?q=selfie&cm=apple%2Fiphone_6

The samples I checked there seemed similar, so I finally decided this is just how iPhone photos are and moved on.

I ran wget recursive mode to capture any other files linked I may have missed:

```Shell
root@kali# wget -r --level=15 http://ctf-2019...
```

However, this just got me the files I had already found, nothing new.

I ran a directory buster to see if there are any other files/directories on the website...
But seems like that isn't going to find anything...

```Shell
root@kali# gobuster -w ./directory-list-2.3-small.txt -x php,html,png,jpg -t 1 -u http://ctf-2019... | tee gobuster.txt

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://ctf-2019...
[+] Threads      : 1
[+] Wordlist     : ./directory-list-2.3-small.txt
[+] Status codes : 301,302,307,200,204
[+] Extensions   : .php,.html,.png,.jpg
=====================================================
```

But it also didn't find anything new.

I ran more stegnography tools on the selfie and logo images, there was some potentially interesting data in EXIF but comparing it to other files that seemed normal so I moved on.

At this point I tried logging into the SSH service with the username and was going to guess passwords, but that wasn't necessary as the chellange was something else entirely...

```Shell
root@kali# ssh doubledipper@ctf-2019... -p 9003
These 3 look interesting:>>
1830:Y--
<<

root@kali# ssh doubledipper@ctf-2019... -p 9003
These 3 look interesting:>>
1833:---
<<
```

Each time I connect there is a number, a colon and some characters.

I tried more times and kept seeing the number incrementing and new characters.

Note: I'm missing some notes for exactly how it worked from this point, but it seems like connecting as doubledipper user incremented the sequence number, then the next connection attempt would get you a new sequence number and string.

So the challenge seems to require me to capture all the characters and put them together in sequence, using the numbers.

As this was a live CTF with other players, if the sequence increases by connections its possible I will miss some characters which they'll see instead of me, so I need to automate capturing and have it retry until it has all parts.

I write a python script to connect, capture the characters, save them in a local file and then loop.

```Python
#!/usr/bin/env python3

import csv
import os
import shlex
import subprocess
import sys
import time

from collections import defaultdict

import paramiko


def doubledip(address, port):
    command_line = f'ssh -4 -N -n -o PasswordAuthentication=no doubledipper@{address} -p {port}'
    command_args = shlex.split(command_line)
    process = subprocess.Popen(
        command_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output = process.communicate()

    return


def grab_banner(address, port):
    command_line = f'ssh -4 -N -n -o PasswordAuthentication=no foo@{address} -p {port}'
    command_args = shlex.split(command_line)
    process = subprocess.Popen(
        command_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output = process.communicate()

    lines = output[1].decode().strip().split('\n')

    return lines


def main():
    filename = "chunks.csv"

    # create file if it does not exist
    with open(filename, "a") as hdl:
        pass

    chunks = defaultdict(str)
    with open(filename, "r") as hdl:
        reader = csv.reader(hdl)
        for row in reader:
            chunks[row[0]] = row[1]

    for chunk in sorted(chunks):
        print(chunk, chunks[chunk])

    with open(filename, "a") as hdl:
        writer = csv.writer(hdl, lineterminator="\n")

        while True:
            doubledip('ctf-2019...', 9003)
            banner = grab_banner('ctf-2019...', 9003)
            if not banner:
                sys.exit(-1)
            tokens = banner[1].strip().split(":")
            pos = tokens[0]
            val = tokens[1]
            if pos not in chunks:
                chunks[pos] = val
                writer.writerow([pos, val])
                hdl.flush()
                print(f"[{pos}:{val}]", end='')
            else:
                print(".", end='')
            sys.stdout.flush()


if __name__ == '__main__':
    main()
```

The script didn't need to care about the boundaries of the sequence numbers, I just let it run and I would kill it when I saw it appeared to have all the necessary elements.

As it ran, I saw a familiar string...

```Shell
1794 tAQ
1797 IDB
1800 AUG
1803 ---
1806 --E
1809 ND
1812 OPE
1815 NSS
1818 H P
```

Once done, I needed to merge the text parts together in sequence, so I used another script:

```Python
#!/usr/bin/env python3

import csv
import sys
import re
from textwrap import wrap


def main():
    filename = "chunks.csv"

    with open(filename, "r") as hdl:
        reader = csv.reader(hdl)

        positions = dict()

        for row in reader:
            pos = int(row[0])
            val = row[1]

            positions[pos] = val

        max_pos = max(positions.keys())

        output = ''
        missing_chunks = set()
        for i in range(0, max_pos, 3):
            if i in positions:
                output += positions[i]
            else:
                output += '...'
                missing_chunks.add(i)

        # a little fixup based on how we know the file should look
        output = output.replace('ATEKEY', 'ATE KEY')
        output = output.replace('ENDOPEN', 'END OPEN')
        output = re.sub(r' KEY(-+)', " KEY-----\n", output)
        output = output.replace('-----END', "\n-----END")

        lines = output.split("\n")
        new_lines = list()
        new_lines.append(lines[0])
        key_lines = wrap(lines[1], 70)
        for key_line in key_lines:
            new_lines.append(key_line)
        new_lines.append(lines[2])

        print("\n".join(new_lines))

        if missing_chunks:
            print()
            print("WARNING: Missing chunks: %s" % ','.join([str(i) for i in sorted(missing_chunks)]))


if __name__ == '__main__':
    main()
```

This gave us an RSA private key that I saved to a local file, then logged in to SSH using:

```Shell
root@kali# ssh -i id_rsa doubledipper@ctf-2019... -p 9003
These 3 look interesting:>>
1725:h4a
<<
Welcome back doubledipper!  You looking for the flag?

flag{N0t_Ev3ry_thin8_[i,a]s_it_s33ms}

Connection to ctf-2019... closed.
```
