# 01 Reversing1

Here is a binary (reversing100) and its output.

The binary also takes a keyfile (not given) and reads input on stdin. Find the input that produces the output.

## Write-up

Under normal operations, the binary expects a filename argument (the keyfile) and then when running you type something into it to get the output matching outfile.  So we need to find both a good keyfile and input string.

Running the file with no argument or junk filename doesn't do anything interesting.
```Shell
% ./reversing100
can't open keyfile: Bad address
% ./reversing100 1
can't open keyfile: No such file or directory
```

I tried using `strings` on the binary, hoping for a clue, but it doesn't seem to include anything interesting.

Running the binary with an empty file just parrots back the input string:
```Shell
% touch empty

% ./reversing100 empty
hello    <-- my input (stdin)
hello    <-- program output
```

Here is an example of running the binary with a file of zeros.

```Shell
% echo "00000000000000000000000000" > input0
% ./reversing100 input0
hello    <-- my input
XU\\_:   <-- program output
```

Rather than creating a file each time for testing, we can use some bash magic:
```Shell
root@kali# ./reversing100 <(echo -n "0")
hello
XU\\_:
```

It is probably safe to assume the input (stdin) should start with "flag". So to start with we can use this as the input string and compare that with the outfile we have been given.

So when using the input "flag" we'll be looking for output that matches `4>35`, which is the first four characters from the outfile. Although the flag string and the outfile may not be a 1:1 swap per character, this is a starting point.

Loop through ASCII character codes, looking for output that matches:
```Shell
for i in $(seq 1 126); do echo "$i: "; echo -n "flag" | ./reversing100 <(echo -e "\x$i"); echo; done
```

The winner was hex 52, or the character R

```Shell
% ./reversing100 <(echo 'R')
flag
4>35X
```

Though the output includes an extra X at the end that does not match, that is a fifth character so going to ignore it for now.

Using R as the keyfile, input the alphabet and symbols to get their keyed values.

```Shell
% ./reversing100 <(echo 'R')
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()-=_+[]{}\|;:'",<.>/?`~
3016745:;89>?<="# !&'$%*+(

bc`afgdejksqvw
y	)/.ihup~n|l}m2, 
```

Note: The output included some newlines but otherwise was useful.

Now I could manually lookup each value in the outfile and find its corresponding input value.

This came up with: flag{ test flag}

This doesn't quite look right and also failed when submitted.

Looking closer at the outfile, the sixth character is an non-printable character (13) which would not show up when viewing the file as text.
```Shell
% hexdump outfile -C
00000000  34 3e 33 35 29 13 72 26  37 21 26 72 34 3e 33 35  |4>35).r&7!&r4>35|
00000010  2f 58 0a                                          |/X.|
00000013
```

To find the match for this, instead of viewing the program output directly in the terminal, we can output it to a file and look at that through hexdump:
```Shell
echo 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()-=_+[]{}\|;:",<.>/?`~' | ./reversing100 <(echo 'R') > outfile3

% hexdump outfile3 -C
00000000  33 30 31 36 37 34 35 3a  3b 38 39 3e 3f 3c 3d 22  |3016745:;89>?<="|
00000010  23 20 21 26 27 24 25 2a  2b 28 13 10 11 16 17 14  |# !&'$%*+(......|
00000020  15 1a 1b 18 19 1e 1f 1c  1d 02 03 00 01 06 07 04  |................|
00000030  05 0a 0b 08 62 63 60 61  66 67 64 65 6a 6b 72 73  |....bc`afgdejkrs|
00000040  12 71 76 77 0c 74 78 7a  7b 7f 6f 0d 79 09 0f 29  |.qvw.txz{.o.y..)|
00000050  2f 0e 2e 69 68 70 7e 6e  7c 6c 7d 6d 32 2c 58     |/..ihp~n|l}m2,X|
0000005f
```

13 is the 27th character of the input string, which maps to capital letter A.

flag{A test flag}
