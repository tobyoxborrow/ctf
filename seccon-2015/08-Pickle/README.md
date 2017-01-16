# 08 Pickle

To receive the flag you need to send a specially crafted python pickle payload
to an online service. The payload must...

* use only the four pickle opcodes: binint2, list, mark and stop
* be no more than 80 characters
* resolve to a particular result

The source code (minus the flag) was provided.

## Write-up

The source code revealed that the service will take a stream of numbers and
convert them to ASCII characters and then compare the result to the string
"Green and delicious!". Additionally it enforces the rules described in the
introduction.

As with the previous python challenge, it was easier to work in the python
interactive shell for immediate feedback.

References I read to understand the pickle protocol:
* https://docs.python.org/2/library/pickle.html
* http://www.diveintopython3.net/serializing.html

First I checked what a python list looked like pickled.

```
>>> l = [71, 114]
>>> type(l)
<type 'list'>
>>> pickletools.dis(pickle.dumps(l))
    0: (    MARK
    1: l        LIST       (MARK at 0)
    2: p    PUT        0
    5: I    INT        71
    9: a    APPEND
   10: I    INT        114
   15: a    APPEND
   16: .    STOP
highest protocol among opcodes = 0
```

This uses opcodes outside of the restricted set to work with.

If we remove PUT and APPEND, keeping the INT for now...

```
>>> pickletools.dis('(lI71\nI114\n.')
    0: (    MARK
    1: l        LIST       (MARK at 0)
    2: I    INT        71
    6: I    INT        114
   11: .    STOP
highest protocol among opcodes = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/tobyox/.pyenv/versions/2.7.11/lib/python2.7/pickletools.py", line 2025, in dis
    raise ValueError("stack not empty after STOP: %r" % stack)
ValueError: stack not empty after STOP: [list, int_or_bool]
```

It didn't quite like that. From the diveintopython3 link, I saw that a tuple
example had the tuple opcode at the end of the list of integers, but before the
STOP, so I tried something similar.

```
>>> pickletools.dis('(I71\nI114\nl.')
    0: (    MARK
    1: I        INT        71
    5: I        INT        114
   10: l        LIST       (MARK at 0)
   11: .    STOP
highest protocol among opcodes = 0
```

Now I can swap out INT for BININT2 which is a 2 byte integer. The format is
slightly different from INT. I'll need to provide the character values in hex.

```
~ echo -n 'Green and delicious!' | xxd -i
  0x47, 0x72, 0x65, 0x65, 0x6e, 0x20, 0x61, 0x6e, 0x64, 0x20, 0x64, 0x65,
  0x6c, 0x69, 0x63, 0x69, 0x6f, 0x75, 0x73, 0x21
```

Test:

```
>>> import pickletools
>>> pickletools.dis('(M\x47\x00M\x72\x00l.')
    0: (    MARK
    1: M        BININT2    71
    4: M        BININT2    114
    7: l        LIST       (MARK at 0)
    8: .    STOP
```

Another small challenge that is that since the pickle will contain binary
values, it is not so simple to just echo the pickle from the shell to the
challenge service, instead we can cat some file containing the pickle.

```
>>> pp = '(M\x47\x00M\x72\x00M\x65\x00M\x65\x00M\x6e\x00M\x20\x00M\x61\x00M\x6e\x00M\x64\x00M\x20\x00M\x64\x00M\x65\x00M\x6c\x00M\x69\x00M\x63\x00M\x69\x00M\x6f\x00M\x75\x00M\x73\x00M\x21\x00l.'
>>> f = open("save.p", "wb")
>>> f.write(pp)
>>> f.close()

% xxd save.p
00000000: 284d 4700 4d72 004d 6500 4d65 004d 6e00  (MG.Mr.Me.Me.Mn.
00000010: 4d20 004d 6100 4d6e 004d 6400 4d20 004d  M .Ma.Mn.Md.M .M
00000020: 6400 4d65 004d 6c00 4d69 004d 6300 4d69  d.Me.Ml.Mi.Mc.Mi
00000030: 004d 6f00 4d75 004d 7300 4d21 006c 2e    .Mo.Mu.Ms.M!.l.
```

Now we can submit and see the result... (note the challenge was internal and
the host mentioned below is no longer in service).

```
% cat save.p | nc 2015.ctf.captchaflag.com 9004

    Welcome to the Python pickle challenge!

    Enter the correct pickle string, using a restricted subset of opcodes.

    You will need to read the source code for this challenge.
    You may also need to read the standard library's `pickle.py` module.

    flag{hope_it_was_not_too_salty}
```
