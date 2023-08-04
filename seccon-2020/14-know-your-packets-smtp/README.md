# 14 Know your packets smtp

Spam Message Transfer Protocol?

# Design

Uses a common 500MB dump.pcap (of approximately 880,000 packets) used for all
the "Know your packets" challenges.

## Write-up
Loaded up the file into Wireshark.

As this is a low point challenge, assumed traffic will be on the standard SMTP
port 25. Also look for the word "spam" since it is mentioned in the challenge
text.

Adding a wireshark filter:

```
tcp.port == 25 and tcp.payload ~ "spam"
```

This leaves 12 packets.

Following the TCP stream for one of the packets finds a spam email being
accepted for delivery. The email body is long, but did not have any obvious
flag in it.

```
220 8dd669f9318c ESMTP Sendmail 8.15.2/8.15.2/Debian-10; Wed, 29 Aug 2018 01:27:17 GMT; (No UCE/UBE) logging access from: xxxxxxxxxxxx.in-addr.zzxyy.ctf(OK)-xxxxxxxxxxxx.in-addr.zzxyy.ctf [xxxxxxxxxxxx]
HELO spammimic.com
250 8dd669f9318c Hello xxxxxxxxxxxx.in-addr.zzxyy.ctf [xxxxxxxxxxxx], pleased to meet you
MAIL FROM: spammer@spammimic.com
250 2.1.0 spammer@spammimic.com... Sender ok
RCPT TO: root@localhost
250 2.1.5 root@localhost... Recipient ok
DATA
354 Enter mail, end with "." on a line by itself
To: root@localhost
From: spammer@spammimic.com
Subject: Buy 1 spam encoded email, get 1 free

Dear Professional ; Especially for you - this cutting-edge
intelligence ! If you no longer wish to receive our
publications simply reply with a Subject: of "REMOVE"
and you will immediately be removed from our club .
This mail is being sent in compliance with Senate bill
2216 , Title 9 ; Section 306 ! THIS IS NOT MULTI-LEVEL
MARKETING . Why work for somebody else when you can
become rich as few as 60 days ! Have you ever noticed
society seems to be moving faster and faster and people
love convenience . Well, now is your chance to capitalize
on this . We will help you use credit cards on your
website and decrease perceived waiting time by 190%
. You can begin at absolutely no cost to you . But
don't believe us . Prof Simpson who resides in Texas
tried us and says "I was skeptical but it worked for
me" ! We assure you that we operate within all applicable
laws . For the sake of your family order now . Sign
up a friend and you get half off ! God Bless ! Dear
Friend , Your email address has been submitted to us
indicating your interest in our publication . If you
are not interested in our publications and wish to
be removed from our lists, simply do NOT respond and
ignore this mail . This mail is being sent in compliance
with Senate bill 1618 ; Title 2 , Section 301 . This
is not multi-level marketing ! Why work for somebody
else when you can become rich in 58 weeks ! Have you
ever noticed people will do almost anything to avoid
mailing their bills plus most everyone has a cellphone
! Well, now is your chance to capitalize on this !
We will help you SELL MORE and increase customer response
by 170% ! You are guaranteed to succeed because we
take all the risk . But don't believe us . Mr Jones
of Georgia tried us and says "Now I'm rich many more
things are possible" ! This offer is 100% legal ! So
make yourself rich now by ordering immediately ! Sign
up a friend and you'll get a discount of 60% . Best
regards !

.
250 2.0.0 w7T1RHfN000653 Message accepted for delivery
QUIT
221 2.0.0 8dd669f9318c closing connection
```

However, the subject of the mail is "Buy one spam encoded email, get 1 free",
which implies there is perhaps some encoding in use. Perhaps the flag is
encoded into the message using spam wording.

Searching for "encoding messages as spam" finds https://www.spammimic.com/ -
which is the same name as the domain of the sender.

The website can decode a message, just paste it in. The result:

flag{mmm, spam}
