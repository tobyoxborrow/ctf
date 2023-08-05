# 15 Know your packets http-3

Enough to make your brain melt

# Design

Uses the common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

# Write-up
Loaded up the file into Wireshark.

The hint wasn't helpful for what traffic to look for, so I just assumed it may
be in a server response.

I tried another filter, just the successful responses from the server:

```
http and http.response.code == 200
```

Besides the many responses for "GET /" there is also:
* compressed responses for "GET /" (slightly smaller size)
* a GIF from the URL "/flag.not"
* a mysterious 168MB "/file.out" (which has a string "code.out" within it)

I saved the flag.not and flag.out using Wireshark: File -> Export Objects -> HTML

The flag.not appears to be the same flag GIF from the second FTP challenge.
Though they are slightly different. The flag in ftp2 actually has a flag in its
metadata, this one has "this is not a flag!!!" instead. So apparently just here
to slow me down.

The other file is more interesting:

```Shell
% file file.out
file.out: gzip compressed data, was "code.out2", last modified: Wed Aug 29 02:32:02 2018, from Unix, original size modulo 2^32 169111537

% gzip --list file.out
  compressed uncompressed  ratio uncompressed_name
   168870622    169111537   0.1% file.out

% file file
file: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=8308c7c108749687dc192be0eef893ec1b98307e, stripped
```

The file executable is a 7z self-extracting archive another gzip with another
7z SFX and so on.

Manually extracting them a few times reveals the extracted file sizes getting
smaller. One thing I worried about was it was some kind of loop. But it really
seems to be a lot of nested archives. Presumably with a single text file at the
end.

The steps seem fairly repeatable:
* extract gz
* execute binary
* repeat

So I created a shell script to help with that with some checks to make it fail
if the state changes, which may indicate a change in the nesting structure (if
the creator is evil) or the end of the nest.

```bash
#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

COUNT=1

while true
do
    echo "Loop #${COUNT}"

    file=$(file -b code.out)
    if [[ $file != *"gzip compressed data, was"* ]]; then
        echo "code.out is not a gz"
        echo $file
        exit -1
    fi

    mv code.out code.out.gz
    gunzip -t code.out.gz
    gunzip code.out.gz

    mv code.out code.tmp
    chmod +x ./code.tmp
    ./code.tmp

    ls -l code*
    md5sum code*

    rm code.tmp

    COUNT=$((COUNT + 1))
done
```

I let it run and eventually saw this message:

```Shell
Loop #1333
code.out is not a gz
ASCII text, with very long lines
```

The contents are now some BF code:
```Brainfuck
--[----->+<]>.++++++.-----------.++++++.[----->+<]>.-[++>---<]>.+[--->+<]>.[-->+<]>---.++++.--[--->++<]>--.+[----->+<]>.------------.+[--->+<]>+++.-[---->+<]>++.-[--->++<]>--.[--->+<]>---.---.[-->+<]>--.+[-->+<]>++++.--[->++++<]>+.-[----->++<]>.+[--->++<]>-.---.[-->+++++<]>+++.-[--->++<]>--.---.----.+++.>--[-->+++<]>.
```

After a bit of searching I found the `beef` package can probably run this.

```Shell
% apt install beef
% beef code.out
flag{7h15 may hur7 y0ur head}
```
