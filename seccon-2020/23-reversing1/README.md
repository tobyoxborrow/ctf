# 23 Reversing 1

This service is listening on secconctf-2020.example.com:9009. If you give it
the correct password, it will return the flag to you.

# Design

The challenge provides a binary file, reversing100.

```Shell
% file reversing100
reversing100: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, with debug_info, not stripped
```

# Write-up
The strings command is the first choice, but nothing obvious shows up:

```Shell
% strings reversing100 | less
[snip]
GLIBC_2.2.5
fffff.
[]A\A]A^A_
Incorrect password
cisco
Nice try :-)
).+6%695
@y]AANivcXKebB^gFwCZ
accept
16283
```

As the binary is a network service, I'll use radare2 for its static analysis capabilities.

```Shell
r2 reversing100

[0x00400910]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Check for objc references
[x] Check for vtables
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information
[x] Use -AA or aaaa to perform additional experimental analysis.

[0x00400910]> afl
0x00400910    1 41           entry0
0x00400840    1 6            sym.imp.__libc_start_main
0x00400940    4 50   -> 41   sym.deregister_tm_clones
0x00400980    4 58   -> 55   sym.register_tm_clones
0x004009c0    3 28           entry.fini0
0x004009e0    4 38   -> 35   entry.init0
0x00400e50    1 2            sym.__libc_csu_fini
0x00400e54    1 9            sym._fini
0x00400de0    4 101          sym.__libc_csu_init
0x00400a06    3 38           sym.wait_for_zombie
0x00400890    1 6            sym.imp.waitpid
0x00400be3    7 103          sym.take_connections_forever
0x00400b14    8 207          sym.check_pw
0x00400c4a   11 404          main
0x00400810    1 6            sym.imp.memset
0x004008d0    1 6            sym.imp.getaddrinfo
0x004008a0    1 6            sym.imp.perror
0x004008c0    1 6            sym.imp.exit
0x00400900    1 6            sym.imp.socket
0x00400850    1 6            sym.imp.sigemptyset
0x004007e0    1 6            sym.imp.sigaction
0x00400880    1 6            sym.imp.bind
0x004008f0    1 6            sym.imp.freeaddrinfo
0x00400870    1 6            sym.imp.listen
0x00400a2c    4 125          sym.xor_key
0x00400aa9    6 107          sym.const_time_strcmp
0x004007a8    3 26           sym._init
0x00400860    1 6            loc.imp.__gmon_start
0x004007f0    1 6            sym.imp.write
0x00400800    1 6            sym.imp.strlen
0x00400820    1 6            sym.imp.close
0x00400830    1 6            sym.imp.read
0x004008b0    1 6            sym.imp.accept
0x004008e0    1 6            sym.imp.fork
```

We can see a few interesting function names like: check_pw and xor_key

Seek to check_pw and disassemble it:

```Shell
[0x00400910]> s smb.check_pw
[0x00400b14]> pdf
            ; CALL XREF from sym.take_connections_forever @ 0x400c37
┌ 207: sym.check_pw (char *arg1);
│           ; var char *fildes @ rbp-0x114
│           ; var void *buf @ rbp-0x110
│           ; var int64_t var_10h @ rbp-0x10
│           ; var ssize_t var_ch @ rbp-0xc
│           ; var char *ptr @ rbp-0x8
│           ; arg char *arg1 @ rdi
│           0x00400b14      55             push rbp                    ; .//reversing100.c:51
│           0x00400b15      4889e5         mov rbp, rsp
│           0x00400b18      4881ec200100.  sub rsp, 0x120
│           0x00400b1f      89bdecfeffff   mov dword [fildes], edi     ; arg1
│       ┌─< 0x00400b25      e986000000     jmp 0x400bb0                ; .//reversing100.c:56
│       │   ; CODE XREF from sym.check_pw @ 0x400bd3
│      ┌──> 0x00400b2a      c645f000       mov byte [var_10h], 0       ; .//reversing100.c:57
│      ╎│   0x00400b2e      48c745f8640e.  mov qword [ptr], str.Incorrect_password ; .//reversing100.c:58 ; 0x400e64 ; "Incorrect password\n"
│      ╎│   0x00400b36      488d85f0feff.  lea rax, qword [buf]        ; .//reversing100.c:59
│      ╎│   0x00400b3d      4889c6         mov rsi, rax                ; int64_t arg2
│      ╎│   0x00400b40      bf780e4000     mov edi, str.cisco          ; 0x400e78 ; "cisco" ; char *arg1
│      ╎│   0x00400b45      e85fffffff     call sym.const_time_strcmp
│      ╎│   0x00400b4a      85c0           test eax, eax
│     ┌───< 0x00400b4c      7508           jne 0x400b56
│     │╎│   0x00400b4e      48c745f87e0e.  mov qword [ptr], str.Nice_try_: ; .//reversing100.c:60 ; 0x400e7e ; "Nice try :-)\n"
│     │╎│   ; CODE XREF from sym.check_pw @ 0x400b4c
│     └───> 0x00400b56      488d85f0feff.  lea rax, qword [buf]        ; .//reversing100.c:62
│      ╎│   0x00400b5d      4889c6         mov rsi, rax                ; char *arg2
│      ╎│   0x00400b60      bf8c0e4000     mov edi, str.._6_695        ; 0x400e8c ; ").+6%695" ; char *arg1
│      ╎│   0x00400b65      e8c2feffff     call sym.xor_key
│      ╎│   0x00400b6a      488d85f0feff.  lea rax, qword [buf]        ; .//reversing100.c:63
│      ╎│   0x00400b71      4889c6         mov rsi, rax                ; int64_t arg2
│      ╎│   0x00400b74      bf950e4000     mov edi, str.y_AANivcXKebB_gFwCZ ; 0x400e95 ; "@y]AANivcXKebB^gFwCZ" ; char *arg1
│      ╎│   0x00400b79      e82bffffff     call sym.const_time_strcmp
│      ╎│   0x00400b7e      85c0           test eax, eax
│     ┌───< 0x00400b80      750b           jne 0x400b8d
│     │╎│   0x00400b82      488b05070820.  mov rax, qword [obj.Flag]   ; .//reversing100.c:64 ; [0x601390:8]=0
│     │╎│   0x00400b89      488945f8       mov qword [ptr], rax
│     │╎│   ; CODE XREF from sym.check_pw @ 0x400b80
│     └───> 0x00400b8d      488b45f8       mov rax, qword [ptr]        ; .//reversing100.c:66
│      ╎│   0x00400b91      4889c7         mov rdi, rax                ; const char *s
│      ╎│   0x00400b94      e867fcffff     call sym.imp.strlen         ; size_t strlen(const char *s)
│      ╎│   0x00400b99      4889c2         mov rdx, rax                ; size_t nbytes
│      ╎│   0x00400b9c      488b4df8       mov rcx, qword [ptr]
│      ╎│   0x00400ba0      8b85ecfeffff   mov eax, dword [fildes]
│      ╎│   0x00400ba6      4889ce         mov rsi, rcx                ; const char *ptr
│      ╎│   0x00400ba9      89c7           mov edi, eax                ; int fd
│      ╎│   0x00400bab      e840fcffff     call sym.imp.write          ; ssize_t write(int fd, const char *ptr, size_t nbytes)
│      ╎│   ; CODE XREF from sym.check_pw @ 0x400b25
│      ╎└─> 0x00400bb0      488d8df0feff.  lea rcx, qword [buf]        ; .//reversing100.c:56
│      ╎    0x00400bb7      8b85ecfeffff   mov eax, dword [fildes]
│      ╎    0x00400bbd      ba00010000     mov edx, 0x100              ; 256 ; size_t nbyte
│      ╎    0x00400bc2      4889ce         mov rsi, rcx                ; void *buf
│      ╎    0x00400bc5      89c7           mov edi, eax                ; int fildes
│      ╎    0x00400bc7      e864fcffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
│      ╎    0x00400bcc      8945f4         mov dword [var_ch], eax
│      ╎    0x00400bcf      837df400       cmp dword [var_ch], 0
│      └──< 0x00400bd3      0f8f51ffffff   jg 0x400b2a
│           0x00400bd9      bf00000000     mov edi, 0                  ; .//reversing100.c:68 ; int status
└           0x00400bde      e8ddfcffff     call sym.imp.exit           ; void exit(int status)
```Shell


This function looks like it:
	* reads in the user input
	* checks if it is "cisco" and if it does it changes the failure message (but doesn't quit here)
	* XORs the user input with ").+6%695" (using the function xor_key)
	* Compares the XORed input with "@y]AANivcXKebB^gFwCZ"

The xor_key function:

```Shell
┌ 125: sym.xor_key (char *arg1, char *arg2);
│           ; var char *s @ rbp-0x20
│           ; var char *var_18h @ rbp-0x18
│           ; var size_t var_ch @ rbp-0xc
│           ; var size_t var_8h @ rbp-0x8
│           ; var int64_t var_4h @ rbp-0x4
│           ; arg char *arg1 @ cf
│           ; arg char *arg2 @ rip
│           0x00400a2c      55             push rbp                    ; .//reversing100.c:30
│           0x00400a2d      4889e5         mov rbp, rsp
│           0x00400a30      4883ec20       sub rsp, 0x20
│           0x00400a34      48897de8       mov qword [var_18h], rdi    ; arg1
│           0x00400a38      488975e0       mov qword [s], rsi          ; arg2
│           0x00400a3c      488b45e0       mov rax, qword [s]          ; .//reversing100.c:32
│           0x00400a40      4889c7         mov rdi, rax                ; const char *s
│           0x00400a43      e8b8fdffff     call sym.imp.strlen         ; size_t strlen(const char *s)
│           0x00400a48      8945f8         mov dword [var_8h], eax
│           0x00400a4b      488b45e8       mov rax, qword [var_18h]    ; .//reversing100.c:33
│           0x00400a4f      4889c7         mov rdi, rax                ; const char *s
│           0x00400a52      e8a9fdffff     call sym.imp.strlen         ; size_t strlen(const char *s)
│           0x00400a57      8945f4         mov dword [var_ch], eax
│           0x00400a5a      c745fc000000.  mov dword [var_4h], 0       ; .//reversing100.c:34
│       ┌─< 0x00400a61      eb3c           jmp 0x400a9f
│       │   ; CODE XREF from sym.xor_key @ 0x400aa5
│      ┌──> 0x00400a63      8b45fc         mov eax, dword [var_4h]     ; .//reversing100.c:35
│      ╎│   0x00400a66      4863d0         movsxd rdx, eax
│      ╎│   0x00400a69      488b45e0       mov rax, qword [s]
│      ╎│   0x00400a6d      488d0c02       lea rcx, qword [rdx + rax]
│      ╎│   0x00400a71      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x00400a74      4863d0         movsxd rdx, eax
│      ╎│   0x00400a77      488b45e0       mov rax, qword [s]
│      ╎│   0x00400a7b      4801d0         add rax, rdx
│      ╎│   0x00400a7e      0fb630         movzx esi, byte [rax]
│      ╎│   0x00400a81      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x00400a84      99             cdq
│      ╎│   0x00400a85      f77df4         idiv dword [var_ch]
│      ╎│   0x00400a88      89d0           mov eax, edx
│      ╎│   0x00400a8a      4863d0         movsxd rdx, eax
│      ╎│   0x00400a8d      488b45e8       mov rax, qword [var_18h]
│      ╎│   0x00400a91      4801d0         add rax, rdx
│      ╎│   0x00400a94      0fb600         movzx eax, byte [rax]
│      ╎│   0x00400a97      31f0           xor eax, esi
│      ╎│   0x00400a99      8801           mov byte [rcx], al
│      ╎│   0x00400a9b      8345fc01       add dword [var_4h], 1       ; .//reversing100.c:34
│      ╎│   ; CODE XREF from sym.xor_key @ 0x400a61
│      ╎└─> 0x00400a9f      8b45fc         mov eax, dword [var_4h]
│      ╎    0x00400aa2      3b45f8         cmp eax, dword [var_8h]
│      └──< 0x00400aa5      7cbc           jl 0x400a63
│           0x00400aa7      c9             leave                       ; .//reversing100.c:37
└           0x00400aa8      c3             ret
```

Because it is XOR, which in theory you can feed in the output string and it'll
return the input string.

Using gdb you can step through and try it. I tried this but the string I got
back was pseudo random and didn't work so I assumed the xor_pw function did a
bit more.

I created a python file to simulate the function as I wasn't sure of my
disassembly skills. But they were correct.

I read through it carefully and it really did seem to be just using XOR. Then I
realised I'm passing a newline as part of my string and that was the problem.
Instead of using netcat (nc) and manually typing and hitting return, you can
echo the string without a newline to nc:

```Shell
$ echo 'iWvwdxPCJv`SGtgRoYhl' | nc secconctf-2020.example.com 9009
flag{857e6d597797ff32698888384ef59586}
```
