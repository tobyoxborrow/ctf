# 03 Password

The program file `93ee82f2be8ca0c9008c669aee1056d1` will reveal the key when
provided the correct password.

## Write-up

Initially ran `strings` on the program and saw some useful output:

```
Error: Must supply a password as an argument.
Error: Please supply only one password.
You found me!
Try again
```

I mistakenly assumed the string "You found me!" was text that would be output
by the program when you provided it the correct password, so didn't try it.

So I went to gdb and followed the program to see when it compared the user
input. The following segment shows a function called `decode_flag`, so we can
assume the previous test and jump are where the user input is actually tested.

```
=> 0x8048670 <main+81>: test   %eax,%eax
   0x8048672 <main+83>: jne    0x804867b <main+92>
   0x8048674 <main+85>: call   0x80484ed <decode_flag>
   0x8048679 <main+90>: jmp    0x8048687 <main+104>
   0x804867b <main+92>: movl   $0x804878a,(%esp)
```

How about we just erase all that nonsense about checking the user input and
just slide into the decode_flag function... we won't even need to know the
password:

```
(gdb) set write
set write
(gdb) set {unsigned int}$pc = 0x909090
set {unsigned int}$pc = 0x909090
(gdb) set {unsigned char}($pc+3) = 0x90
set {unsigned char}($pc+3) = 0x90
(gdb) set write off
set write off
(gdb) x/10i $pc
x/10i $pc
=> 0x8048670 <main+81>: nop
   0x8048671 <main+82>: nop
   0x8048672 <main+83>: nop
   0x8048673 <main+84>: nop
   0x8048674 <main+85>: call   0x80484ed <decode_flag>
   0x8048679 <main+90>: jmp    0x8048687 <main+104>
   0x804867b <main+92>: movl   $0x804878a,(%esp)
   0x8048682 <main+99>: call   0x80483a0 <puts@plt>
   0x8048687 <main+104>:        mov    $0x0,%eax
   0x804868c <main+109>:        leave

(gdb) c
c
Continuing.
flag{strings_is_awsome}
```

After seeing the flag, I went back and tried the output from strings and found
"You found me!" was in fact the password.

Although the actual solution should have been easier, this is also pretty much
the first time I've really used gdb and I felt the experience was worthwhile.

Just as extra experience, I poked around to see if the program compared the
user-input in plain-text and it did.

```
gdb$ stepi
--------------------------------------------------------------------------[regs]
  EAX: 0x0804877C  EBX: 0xB7FCF000  ECX: 0x531E18EF  EDX: 0xBFFFF8A7  o d I t S z a p C 
  ESI: 0x00000000  EDI: 0x00000000  EBP: 0x0000000D  ESP: 0xBFFFF688  EIP: 0xB7F5FF50
  CS: 0073  DS: 007B  ES: 007B  FS: 0000  GS: 0033  SS: 007B  Jump is taken (c=1)
--------------------------------------------------------------------------[code]
=> 0xb7f5ff50 <__strncmp_ssse3+16>:     jb     0xb7f61790 <__strncmp_ssse3+6224>
   0xb7f5ff56 <__strncmp_ssse3+22>:     mov    ecx,edx
   0xb7f5ff58 <__strncmp_ssse3+24>:     and    ecx,0xfff
   0xb7f5ff5e <__strncmp_ssse3+30>:     cmp    ecx,0xff0
   0xb7f5ff64 <__strncmp_ssse3+36>:     ja     0xb7f5ffba <__strncmp_ssse3+122>
   0xb7f5ff66 <__strncmp_ssse3+38>:     mov    ecx,eax
   0xb7f5ff68 <__strncmp_ssse3+40>:     and    ecx,0xfff
   0xb7f5ff6e <__strncmp_ssse3+46>:     cmp    ecx,0xff0
--------------------------------------------------------------------------------
238     in ../sysdeps/i386/i686/multiarch/strcmp-ssse3.S
gdb$ x /4bs 0x0804877C
0x804877c:      "You found me!"
0x804878a:      "Try again"
0x8048794:      "\001\033\003;0"
0x804879a:      ""
```
