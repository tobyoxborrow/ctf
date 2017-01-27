# 20 Set Up

To receive the flag you need to send a specially crafted input to an online
service. The string must...

* evaluate to an empty `set`
* be up to 12 characters
* only use the characters: a-d 3 f-z {} []

The source code for the service (minus the flag) was provided.

## Write-up

The source code does not reveal anything useful. But allows you to test
locally. Despite having the script I chose to use the python interpreter as it
provides a faster feedback loop.

The limited character set notably does not include the letter "e" which would
be necessary to write the statement "set()".

I found some other ways to create sets on [stack
overflow](http://stackoverflow.com/questions/6130374/empty-set-literal-in-python#6130391).

One of the alternative answers mentions:

```
{1,2,3}.__class__
<type 'set'>
```

We have { 3 and } so something along these lines seems plausible. Though `{3}`
would result in a set with a single element, 3.

I iterated on the idea. At one point I found python will return the difference
of two sets, and if they are identical you'll get an empty set. Though this is
not the solution (needs the "-" character) perhaps useful to know.
```
>>> {3}-{3}
set()
```

Soon I found using a list comprehension for loop within curly braces would
return a set with the result of the loop. And if you used an empty list, the
result of the loop would be empty so the set would be empty. This doesn't work
because of the spaces though...
```
>>> {i for i in []}
set()
```

Example with values to illustrate how this may be used in normal code:
```
>>> {i for i in [1,2,"a"]}
{1, 2, 'a'}
```

I can't just remove the spaces in the above since python will interpret
"iforiin" as a single token. If this is to work I need to remove the spaces but
still let python interpret the tokens in the statement separately. The brackets
would help terminate tokens and I played with some ideas of that.

Eventually I found this works, though I'm lost for how to interpret it. It is
probably close to the solution since it uses all the valid characters but is
slightly too long.
```
>>> {[]for[]in[]}
set()
```

Trying this with values doesn't work, so this isn't being handled by python
quite the same as the above code. The "int" the below error is referring to is
the first value (1) from the list.
```
>>> {[]for[]in[1,2,"a"]}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <setcomp>
TypeError: 'int' object is not iterable
```

Playing around some more I eventually found the following. Again I'm not
exactly sure how to interpret the code, but the 3 is treated as a number and
distinct from the for token.
```
>>> {3for[]in[]}
set()
```

It is short enough, submit...

```
% echo -n "{3for[]in[]}" | nc ctf-2016.captchaflag.com 9001
flag{on_your_mark_get_set_go}
```

I'm not sure if that's the official solution, but it works.
