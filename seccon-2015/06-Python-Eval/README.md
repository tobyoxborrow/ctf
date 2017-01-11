# 06 Python Eval Filter

To receive the flag you need to send a specially crafted input to an online
service. The string must...

* evaluate to the `code` type
* be up to 40 characters
* only use the characters: a-z 0-9 _ . : []

The source code (minus the flag) is provided.

## Write-up

The source code does not reveal anything useful, it just enforces the rules
described in the introduction. However, it does at least allow you to quickly
check attempts before submitting them to the online service.

That said, instead of trying inputs with the script, I thought it would be
easier to use python in an interactive mode so that the feedback loop is
faster.

Since we need a code object, lambda seemed like a good starting point. The
statement `lambda x: 0` is a lambda function that returns 0, this is as small
as I think they can be. So that was the starting point. This statement returns
a function.

```
>>> lambda x: 0
<function <lambda> at 0x10f51c5f0>
```

Next some poking around trying to get the code type out of that using
introspection.

Though we can't access properties on the statement as-is.

```
>>> lambda x: 0.__code__
  File "<stdin>", line 1
    lambda x: 0.__code__
                       ^
SyntaxError: invalid syntax
```

So I put it in an anonymous list and referenced the first (and only) element of
that list.

```
>>> [lambda x: 0]
[<function <lambda> at 0x10f51c668>]
>>> [lambda x: 0][0].__code__
<code object <lambda> at 0x10f500c30, file "<stdin>", line 1>
>>> [lambda:0][0].__code__
<code object <lambda> at 0x10f5008b0, file "<stdin>", line 1>
>>> dir([lambda:0][0].__code__)
['__class__', '__cmp__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames']
>>> [lambda:0][0].__code__.__class__
<type 'code'>
```
