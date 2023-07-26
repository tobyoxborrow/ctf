# 10 Reversing 2

Here is a binary and its output. The binary also takes a keyfile (not given) and reads input on stdin. Find the input that produces the output.

## Design

The challenge provided two files, a binary file called reversing200 and a data file called outfile.

```Shell
% file reversing200
reversing200: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, stripped
% file outfile
outfile: data
```

This challenge appears similar to the earlier reversing challenge in the same event.

To solve the challenge, you would need to come up with two values, the key file and the input on stdin.

## Write-up

The outfile contains a single line of apparently random characters.

```Shell
root@kali# wc -c outfile
63 outfile
root@kali# hexdump outfile -C
00000000  1d 4e 54 58 49 29 39 24  52 62 63 2f 47 4d 57 48  |.NTXI)9$Rbc/GMWH|
00000010  5f 52 35 03 74 57 28 5c  58 43 47 39 57 51 68 65  |_R5.tW(\XCG9WQhe|
00000020  6e 48 43 24 47 67 59 37  43 3b 57 44 58 65 42 3a  |nHC$GgY7C;WDXeB:|
00000030  46 57 56 62 11 41 36 4d  65 5f 7d 75 52 59 58     |FWVb.A6Me_}uRYX|
0000003f
```

As with the earlier reversing challenge, there are non-ascii characters in there, which would not show up if the file was viewed in a text editor.

I examined the binary in radare2 to understand how it works.
```Shell
r2 ./reversing200

s main
VV
```

main() reads 7 characters from the keyfile
And reads 7 characters from stdin, implies key should be a multiple of 7
The outfile is 63 characters long (wc -c outfile) which goes into 7 9 times.

Behaviour review:

I tried some sample input key files with sizes smaller than 7 characters to see how the binary acted.

```Shell
root@kali# cat keyfile1 keyfile2 keyfile3 keyfile4 keyfile5 keyfile6
R
RR
RRR
RRRR
RRRRR
RRRRRR

root@kali# echo "flag{777}" | ./reversing200 keyfile1 | xargs
8vag{77
root@kali# echo "flag{777}" | ./reversing200 keyfile2 | xargs
8>kg{77 O
root@kali# echo "flag{777}" | ./reversing200 keyfile3 | xargs
8>3q{77 O
root@kali# echo "flag{777}" | ./reversing200 keyfile4 | xargs
8>3977 OV
root@kali# echo "flag{777}" | ./reversing200 keyfile5 | xargs
8>39MA7 OVV
root@kali# echo "flag{777}" | ./reversing200 keyfile6 | xargs
8>39M A OVVV
```

And again with key files larger than 7 characters:

```Shell
root@kali# cat keyfile7 keyfile14 keyfile21
RRRRRRR
RRRRRRRRRRRRRR
RRRRRRRRRRRRRRRRRRRRR

root@kali# echo "flag{777}" | ./reversing200 keyfile7 | xargs
8>39M OVVVV
root@kali# echo "flag{777}" | ./reversing200 keyfile14 | xargs
8>39M OVVVV
root@kali# echo "flag{777}" | ./reversing200 keyfile21 | xargs
8>39M OVVVV
root@kali#
```

Observation: The key file doesn't change the output if it is longer than 7 characters.

I'm assuming the input string is the correct flag. "flag{}" is 6 characters already, so the input string is likely longer than 7 characters, perhaps also 63 characters like the outfile.

I created some sample input files to try:

```Shell
root@kali# echo -n "flag{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}" > input
root@kali# wc -c input
63 input

# getting some random input
root@kali# head -c 500 /dev/random | tr -dc 'a-zA-Z' | head -c 63 > input2
root@kali# wc -c input2
63 input2
```

We can see single characters will output as the same character:

```Shell
root@kali# cat input | ./reversing200 keyfile | xargs
8>39M333333333333333333333333333333333333333333333333333333333OYYYYYYY
```

I then opened up radare2 again to spend more time understanding the code.

```Shell
root@kali# r2 ./reversing200
[0x00400520]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[x] Type matching analysis for all functions (aaft)
[x] Use -AA or aaaa to perform additional experimental analysis.
[0x00400520]> s main
[0x00400684]> pdf

[...cut for brievity...]
```

I found where the program branches off, gets chunks of 7 chars runs a little "encryption" method and loops to the next 7 chars.
But if the chunk is smaller (presumably the last few chars of input) it follows a different branch, doing extra processing before then following the normal "encryption" path as if it were 7 chars.

Assumption: the input might not be a perfect multiple of 7, the last chunk could be smaller, just to add an extra challenge.

Here is function fcn.00400616, which appears to do the encryption. I've annotate the code as comments on the right.

```Assembly
/ (fcn) fcn.00400616 110
|   fcn.00400616 (int arg1, int arg2, int arg3);
|           ; var int local_28h @ rbp-0x28
|           ; var int local_20h @ rbp-0x20
|           ; var int local_18h @ rbp-0x18
|           ; var int local_4h @ rbp-0x4
|           ; arg int arg1 @ dx
|           ; arg int arg2 @ ch
|           ; arg int arg3 @ bh
|           ; CALL XREF from main (0x40074d)
|           0x00400616      55             push rbp
|           0x00400617      4889e5         mov rbp, rsp
|           0x0040061a      48897de8       mov qword [local_18h], rdi   ; arg1  input chunk: flag{a}
|           0x0040061e      488975e0       mov qword [local_20h], rsi   ; arg2  keyfile RRRRRRR
|           0x00400622      488955d8       mov qword [local_28h], rdx   ; arg3  number, initially 1, probably input character index
|           0x00400626      c745fc000000.  mov dword [local_4h], 0      ; probably a loop counter over the input chunk
|       ,=< 0x0040062d      eb4d           jmp 0x40067c                 ; while i < 7:
|       |   ; CODE XREF from fcn.00400616 (0x400680)
|      .--> 0x0040062f      8b45fc         mov eax, dword [local_4h]    ; set eax to loop index (0 on first iteration)
|      :|   0x00400632      4863d0         movsxd rdx, eax              ; set rdx to eax (loop index) - with sign extension (0 on first iteration)
|      :|   0x00400635      488b45d8       mov rax, qword [local_28h]   ; set rax to input character index (1 on first iteration)
|      :|   0x00400639      488d0c02       lea rcx, qword [rdx + rax]   ; set rcx to sum of loop index and character index (0+1=1 on first iteration)
|      :|   0x0040063d      8b45fc         mov eax, dword [local_4h]    ; set eax to loop index (again, 0 on first iter)
|      :|   0x00400640      4863d0         movsxd rdx, eax              ; set rdx to eax (again)
|      :|   0x00400643      488b45e8       mov rax, qword [local_18h]   ; set rax to ptr of input chunk
|      :|   0x00400647      4801d0         add rax, rdx                 ; add loop index to ptr of input chunk (no change)
|      :|   0x0040064a      0fb600         movzx eax, byte [rax]        ; set eax to first byte of user input chunk ("f")
|      :|   0x0040064d      0fbed0         movsx edx, al                ; set edx to first byte of user input chunk ("f")
|      :|   0x00400650      8b45fc         mov eax, dword [local_4h]    ; set eax to loop index (again, 0 on first iter)
|      :|   0x00400653      4863f0         movsxd rsi, eax              ; set rsi to loop index (0 on first iter)
|      :|   0x00400656      488b45e0       mov rax, qword [local_20h]   ; set rax to ptr of keyfile chunk
|      :|   0x0040065a      4801f0         add rax, rsi                 ; add loop index to ptr of keyfile chunk (no change on first iter)
|      :|   0x0040065d      0fb600         movzx eax, byte [rax]        ; set eax to first byte of keyfile ("R")
|      :|   0x00400660      0fbec0         movsx eax, al                ; set eax to first byte of keyfile ("R")
|      :|   0x00400663      01c2           add edx, eax                 ; add (ascii code) of first letter of keyfile to first letter of input (R=0x52 + f=0x66 = 0xb8)
|      :|   0x00400665      89d0           mov eax, edx                 ; set eax to "keyed" char
|      :|   0x00400667      c1f81f         sar eax, 0x1f                ; shift arithmetic right keyed char by 0x1f (31) (divide by 2 31 times) (result is 0 on first iter)
|      :|   0x0040066a      c1e819         shr eax, 0x19                ; shift logical right (divide) keyed char by 0x19 (25) (divide by 2 25 times) (result is 0 on first iter)
|      :|   0x0040066d      01c2           add edx, eax                 ; add shifted char to keyed char (0x0 + 0xb8 = 0xb8, no change)
|      :|   0x0040066f      83e27f         and edx, 0x7f                ; AND 0x7f (127, lower 7 bits set) to keyed char (0xb8 AND 0x7f = 0x38: ascii '8')
|      :|   0x00400672      29c2           sub edx, eax                 ; subtract eax from edx (8 - 0 = 8)
|      :|   0x00400674      89d0           mov eax, edx                 ; set eax to "encrypted" char
|      :|   0x00400676      8801           mov byte [rcx], al           ; set rcx to "encrypted" char
|      :|   0x00400678      8345fc01       add dword [local_4h], 1      ; increment loop counter
|      :|   ; CODE XREF from fcn.00400616 (0x40062d)
|      :`-> 0x0040067c      837dfc06       cmp dword [local_4h], 6
|      `==< 0x00400680      7ead           jle 0x40062f
|           0x00400682      5d             pop rbp
\           0x00400683      c3             ret
```

Now knowing the logic, I wrote a script that would first find keyfile values from the outfile and check if they matched the assumed keyfile values.

Assumptions:
* The first 5 characters of the keyfile: flag{
* Some padding at the end of the string probably means we can't assume the last character of the outfile is }

Additionally I tried all permutations of keyfile characters 6 and 7. Because we
have multiple characters in the outfile that will be encrypted with the same
keyfile character (skipping the last chunk of 7 characters, due to potential
padding), we could then intersect each outfile character to reduce the number
of valid combinations.  However, even after reducing the combinations this was
over 1000 keyfile combinations and would take too long.

The problem is we only know the outfile characters, and have to guess all
possible keyfile and input characters.

So instead we could have the script decrypt the characters it can do with the
partial keyfile. Once we have that, it may be possible to just guess the
remainder by seeing incomplete words in the decrypted string.

Sure enough, after decrypting the string with a partial keyfile we get:
```Shell
root@kali# ./decrypt.py
keyfile:    7bsqN
plain-text: flag{..mpora.. flag.. Figu.. out ..methi.. bett.. to s..®}..
```

I guessed the first missing input characters are: "Te" (to spell Temporary)...

```Shell
root@kali# ./decrypt.py
keyfile:    7bsqNUT
plain-text: flag{Temporary flag.  Figure out something better to say®}
```

This appears to have almost solve it.  I found one small logic error... when decrypting characters it would accept values > 0x7e, so fixing that...

```Shell
 0  0  '\x1d'  7  f 102  0x66
 1  1     'N'  b  l 108  0x6c
 2  2     'T'  s  a  97  0x61
 3  3     'X'  q  g 103  0x67
 4  4     'I'  N  { 123  0x7b
 5  5     ')'  U  T  84  0x54
 6  6     '9'  T  e 101  0x65
 7  0     '$'  7  m 109  0x6d
 8  1     'R'  b  p 112  0x70
 9  2     'b'  s  o 111  0x6f
10  3     'c'  q  r 114  0x72
11  4     '/'  N  a  97  0x61
12  5     'G'  U  r 114  0x72
13  6     'M'  T  y 121  0x79
14  0     'W'  7     32  0x20
15  1     'H'  b  f 102  0x66
16  2     '_'  s  l 108  0x6c
17  3     'R'  q  a  97  0x61
18  4     '5'  N  g 103  0x67
19  5  '\x03'  U  .  46  0x2e
20  6     't'  T     32  0x20
21  0     'W'  7     32  0x20
22  1     '('  b  F  70  0x46
23  2    '\\'  s  i 105  0x69
24  3     'X'  q  g 103  0x67
25  4     'C'  N  u 117  0x75
26  5     'G'  U  r 114  0x72
27  6     '9'  T  e 101  0x65
28  0     'W'  7     32  0x20
29  1     'Q'  b  o 111  0x6f
30  2     'h'  s  u 117  0x75
31  3     'e'  q  t 116  0x74
32  4     'n'  N     32  0x20
33  5     'H'  U  s 115  0x73
34  6     'C'  T  o 111  0x6f
35  0     '$'  7  m 109  0x6d
36  1     'G'  b  e 101  0x65
37  2     'g'  s  t 116  0x74
38  3     'Y'  q  h 104  0x68
39  4     '7'  N  i 105  0x69
40  5     'C'  U  n 110  0x6e
41  6     ';'  T  g 103  0x67
42  0     'W'  7     32  0x20
43  1     'D'  b  b  98  0x62
44  2     'X'  s  e 101  0x65
45  3     'e'  q  t 116  0x74
46  4     'B'  N  t 116  0x74
47  5     ':'  U  e 101  0x65
48  6     'F'  T  r 114  0x72
49  0     'W'  7     32  0x20
50  1     'V'  b  t 116  0x74
51  2     'b'  s  o 111  0x6f
52  3  '\x11'  q     32  0x20
53  4     'A'  N  s 115  0x73
54  5     '6'  U  a  97  0x61
55  6     'M'  T  y 121  0x79
56  0     'e'  7  .  46  0x2e
57  1     '_'  b  } 125  0x7d
58  2     '}'  s
  10   0xa
59  3     'u'  q     4   0x4
60  4     'R'  N     4   0x4
61  5     'Y'  U     4   0x4
62  6     'X'  T     4   0x4
keyfile:    7bsqNUT
            012345601234560123456012345601234560123456012345601234560123456
plain-text: flag{Temporary flag.  Figure out something better to say.}

outfile:    NTXI)9$Rbc/GMWH_R5tW(\XCG9WQhenHC$GgY7C;WDXeB:FWVbA6Me_}uRYX
```

flag{Temporary flag.  Figure out something better to say.}
