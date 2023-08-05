# 17 My encryption is rusty

You have managed to gain a network foothold on a pentest of the 'Bizcorp' internal network.

There is only one currently known user a maintenance account named 'maintenance'.

Hint #1: "bizcorp is has a very bad password policy."

Hint #2: "bizcorp has decided to follow Cisco by using their own version of the 'secure' cisco default password."

Hint #3: "Intel also likes this style of password, especially for encrypting zip files."

# Design

The challenge is running server running SSH.

# Writeup

Based on the hints, I believed the passwords were probably like: Bizcorp123 or bizcorp123.

Sure enough, bizcorp123 worked:

```Shell
$ ssh -p 9027 maintenance@secconctf-2020.example.com
maintenance@secconctf-2020.example.com's password:
[snip]
maintenance@9b87c37e1db9:~$ ls
flag.txt  irc  mail
maintenance@9b87c37e1db9:~$ file flag.txt
flag.txt: ASCII text
maintenance@9b87c37e1db9:~$ cat flag.txt
```

Very quick, the flag was immediately accessible.

I'm not sure if the flag was meant to be that easy. Since this is a shared
server, another competitor may have done what was necessary and left the flag
here without tidying up. Based on the title and hints I assume the flag may
have been in an encrypted zip file.
