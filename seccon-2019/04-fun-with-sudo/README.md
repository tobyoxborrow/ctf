# 04 Fun with Sudo

You've managed to acquire the creds (audit:audit) to a very limited account on a sensitive server. However, the information you need to access is not available to that user. See what you can do.


## Design

Players login to a normal looking linux server over SSH using the audit user from the challenge text.

There are two files in the user's home directory, flag.txt and hints.txt. The audit user does not have permission to open the flag.txt file.

## Write-up

Unfortunately, due to the design of the challenge, allowing players to login as the same user to a shared linux host, only one player needed to solve it and other users logging in after them can see the results. Or one user could mess the filesystem up and make it unsolvable for other players.

The server state when I played was fairly messed up and there was a file in the home directory containing the flag text so there was essentially nothing to do. But I did look around and work out what was meant to be done...

The title of the challenge mentions sudo, so one of the first things to check are your capabilities:

```
audit@2f15f0ef33fb:~$ sudo -l
[sudo] password for audit:
Matching Defaults entries for audit on 2f15f0ef33fb:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User audit may run the following commands on 2f15f0ef33fb:
    (ALL : ALL) /usr/bin/less /home/audit/hints.txt
```

From this output we can see we can use sudo to run less with a very specific command-line.

One risk of using sudo with commands in this way is that it doesn't take into account those commands can still be used to access other files.

less is typically used to view single files, but it is feature packed can be used to do more.

Presumably, the solution is something like:

```
audit@2f15f0ef33fb:~$ sudo /usr/bin/less /home/audit/hints.txt
(contents of file)
E flag.txt
```

The contents of the hint.txt file don't matter. The idea is that less is now open with elevated privileges and can be used to run commands or access files the original user (audit) could not.

The E (Examine) command in less lets you view the contents of another file.
