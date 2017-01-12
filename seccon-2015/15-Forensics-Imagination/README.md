# 15 Imagination

The flag is in the file `41221d6d81c5df683c1041a1af07d25d`.

## Write-up

The file format is not so easily detected.

```
% file ./41221d6d81c5df683c1041a1af07d25d
./41221d6d81c5df683c1041a1af07d25d: data
```

Have a quick look at the beginning of the file, ICC Profile makes it seem like
some kind of image.

```
% xxd -l 128 ./41221d6d81c5df683c1041a1af07d25d
00000000: 890d 0a1a 0a00 0000 0d49 4844 5200 0003  .........IHDR...
00000010: c000 0002 2a08 0600 0000 eb7e 23cb 0000  ....*......~#...
00000020: 0c18 6943 4350 4943 4320 5072 6f66 696c  ..iCCPICC Profil
00000030: 6500 0048 8995 9707 5853 c916 c7e7 9614  e..H....XS......
00000040: 4242 0b44 404a e84d 905e a5f7 2220 1d6c  BB.D@J.M.^.." .l
00000050: 8424 4028 2104 828a 1d5d 5470 ed22 8aa2  .$@(!....]Tp."..
00000060: a22b 208a ae05 90b5 20a2 5858 042c d817  .+ ..... .XX.,..
00000070: 0b2a 2beb 62c1 86ca 9b14 d0e7 7bfb bdef  .*+.b.......{...
```

I looked at some example working images and saw PNG has the same 0x89 as the
first byte.

I wrote a script to patch the file.

```
% ./repair.py
% file ./41221d6d81c5df683c1041a1af07d25d.png
./41221d6d81c5df683c1041a1af07d25d.png: PNG image data, 960 x 554, 8-bit/color RGBA, non-interlaced
```

Opening the image revealed a screenshot of vim. There wasn't a key in the
format flag{...} so I just tried all the strings I could read in the image and
one of them worked.
