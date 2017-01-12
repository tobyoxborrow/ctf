# 13 Algorithm

The program file `adec6ee0e9deaad89e2dcf2c7198d28c` takes one argument, the
flag itself.

## Write-up

I ran the binary to see the normal behaviour. Since the flags should follow the
format flag{...} I tried that and the output was more descriptive, we can tell
it is trying to process the command-line argument one or more characters at a
time rather than a more simple comparison. Also, note how "ASDFASDF" provides
different output to "foo" or "bar". It seemed like it should be possible to
brute-force the flag.

```
% ./adec6ee0e9deaad89e2dcf2c7198d28c
Error: Must supply the flag as an argument.
% ./adec6ee0e9deaad89e2dcf2c7198d28c foo
Sorry, try again.
% ./adec6ee0e9deaad89e2dcf2c7198d28c bar
Sorry, try again.
% ./adec6ee0e9deaad89e2dcf2c7198d28c ASDFASDF
Failed at index 0 with char A
Sorry, try again.
% ./adec6ee0e9deaad89e2dcf2c7198d28c flag{foo}
Failed at index 5 with char f
Sorry, try again.
```

I ran the binary through strings but did not find anything obvious.

It is also worth noting that the file has been stripped, which makes the
subsequent steps harder.

```
% file adec6ee0e9deaad89e2dcf2c7198d28c
adec6ee0e9deaad89e2dcf2c7198d28c: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0xef920ce9f02c34a2bf80839611cfc3e4d3498536, stripped
```

Next I disassembled the binary and had a quick browse. I came across a block
that looked like it might be handling the flag - a sequence of bytes, possibly
characters followed by a null byte (typical C-style string). Though they do not
actually represent ASCII characters as-is, the range is wrong, they must be
transformed somehow.

```
% objdump -M intel -d adec6ee0e9deaad89e2dcf2c7198d28c > adec6ee0e9deaad89e2dcf2c7198d28c.asm

% less adec6ee0e9deaad89e2dcf2c7198d28c.asm

 804856b:       c6 45 de 99             mov    BYTE PTR [ebp-0x22],0x99
 804856f:       c6 45 df 9c             mov    BYTE PTR [ebp-0x21],0x9c
 8048573:       c6 45 e0 92             mov    BYTE PTR [ebp-0x20],0x92
 8048577:       c6 45 e1 9b             mov    BYTE PTR [ebp-0x1f],0x9b
 804857b:       c6 45 e2 b7             mov    BYTE PTR [ebp-0x1e],0xb7
 804857f:       c6 45 e3 88             mov    BYTE PTR [ebp-0x1d],0x88
 8048583:       c6 45 e4 9a             mov    BYTE PTR [ebp-0x1c],0x9a
 8048587:       c6 45 e5 83             mov    BYTE PTR [ebp-0x1b],0x83
 804858b:       c6 45 e6 9f             mov    BYTE PTR [ebp-0x1a],0x9f
 804858f:       c6 45 e7 8e             mov    BYTE PTR [ebp-0x19],0x8e
 8048593:       c6 45 e8 b0             mov    BYTE PTR [ebp-0x18],0xb0
 8048597:       c6 45 e9 86             mov    BYTE PTR [ebp-0x17],0x86
 804859b:       c6 45 ea 9c             mov    BYTE PTR [ebp-0x16],0x9c
 804859f:       c6 45 eb 8a             mov    BYTE PTR [ebp-0x15],0x8a
 80485a3:       c6 45 ec b1             mov    BYTE PTR [ebp-0x14],0xb1
 80485a7:       c6 45 ed a3             mov    BYTE PTR [ebp-0x13],0xa3
 80485ab:       c6 45 ee af             mov    BYTE PTR [ebp-0x12],0xaf
 80485af:       c6 45 ef 84             mov    BYTE PTR [ebp-0x11],0x84
 80485b3:       c6 45 f0 9a             mov    BYTE PTR [ebp-0x10],0x9a
 80485b7:       c6 45 f1 8c             mov    BYTE PTR [ebp-0xf],0x8c
 80485bb:       c6 45 f2 b0             mov    BYTE PTR [ebp-0xe],0xb0
 80485bf:       c6 45 f3 be             mov    BYTE PTR [ebp-0xd],0xbe
 80485c3:       c7 45 d8 00 00 00 00    mov    DWORD PTR [ebp-0x28],0x0

```

It seems *very* likely this is the key as the 5th and last characters are
probably { and } and their values above are noticeably different from the
majority of the others.

```
f = ASCII 0x66 = flag 0x99 (difference 51)
l = ASCII 0x6c = flag 0x9c (difference 48)
a = ASCII 0x61 = flag 0x92 (difference 49)
g = ASCII 0x67 = flag 0x9b (difference 52)
{ = ASCII 0x7B = flag 0xb7 (difference 60)
```

Next up, gdb.

As I was still unfamiliar with gdb and the binary was stripped finding the
right point to break was a little tricky. After examining the disassembly from
before I assumed the leave/ret opcodes were where the function divides were and
set a breakpoint at 0x8048553 which would be the entry point of the function
where that key block could be found.

```
gdb$ b *0x8048553
Breakpoint 1 at 0x8048553
gdb$ ru
--------------------------------------------------------------------------[regs]
  EAX: 0xBFFFF8EC  EBX: 0xB7FD0FF4  ECX: 0xBFFFF7A4  EDX: 0xBFFFF734  o d I t S z a p c
  ESI: 0x00000000  EDI: 0x00000000  EBP: 0xBFFFF708  ESP: 0xBFFFF6EC  EIP: 0x08048553
  CS: 0073  DS: 007B  ES: 007B  FS: 0000  GS: 0033  SS: 007B
--------------------------------------------------------------------------[code]
=> 0x8048553:	push   ebp
   0x8048554:	mov    ebp,esp
   0x8048556:	push   ebx
   0x8048557:	sub    esp,0x34
   0x804855a:	mov    eax,DWORD PTR [ebp+0x8]
   0x804855d:	mov    DWORD PTR [ebp-0x2c],eax
   0x8048560:	mov    eax,gs:0x14
   0x8048566:	mov    DWORD PTR [ebp-0xc],eax
--------------------------------------------------------------------------------

Breakpoint 1, 0x08048553 in ?? ()
```

Stepping through the code I found the transformation of the users input to the
key around 0x804852d. Here is an example of f (0x66) becoming 0x99:

* 0x66 AND 0xaa (result: 0x22)
    * 0x22 sar/shift-arithmetic-right 1 (result: 0x11)
* 0x66 AND 0x55 (result: 0x44)
    * 0x44 add <itself> (result: 0x88)
* 0x88 OR 0x11 (result: 0x99)

I created a script to perform these same steps on some ASCII characters:

```
% ./translateascii.py
 : 0x10
!: 0x12
": 0x11
#: 0x13
$: 0x18
%: 0x1a
&: 0x19
': 0x1b
(: 0x14
): 0x16
*: 0x15
+: 0x17
,: 0x1c
-: 0x1e
.: 0x1d
/: 0x1f
0: 0x30
1: 0x32
2: 0x31
3: 0x33
4: 0x38
5: 0x3a
6: 0x39
7: 0x3b
8: 0x34
9: 0x36
:: 0x35
;: 0x37
<: 0x3c
=: 0x3e
>: 0x3d
?: 0x3f
@: 0x80
A: 0x82
B: 0x81
C: 0x83
D: 0x88
E: 0x8a
F: 0x89
G: 0x8b
H: 0x84
I: 0x86
J: 0x85
K: 0x87
L: 0x8c
M: 0x8e
N: 0x8d
O: 0x8f
P: 0xa0
Q: 0xa2
R: 0xa1
S: 0xa3
T: 0xa8
U: 0xaa
V: 0xa9
W: 0xab
X: 0xa4
Y: 0xa6
Z: 0xa5
[: 0xa7
\: 0xac
]: 0xae
^: 0xad
_: 0xaf
`: 0x90
a: 0x92
b: 0x91
c: 0x93
d: 0x98
e: 0x9a
f: 0x99
g: 0x9b
h: 0x94
i: 0x96
j: 0x95
k: 0x97
l: 0x9c
m: 0x9e
n: 0x9d
o: 0x9f
p: 0xb0
q: 0xb2
r: 0xb1
s: 0xb3
t: 0xb8
u: 0xba
v: 0xb9
w: 0xbb
x: 0xb4
y: 0xb6
z: 0xb5
{: 0xb7
|: 0xbc
}: 0xbe
~: 0xbd
```

With the above, the key could be worked out:

```
flag{DeCoMpIlErS_HeLp}
```
