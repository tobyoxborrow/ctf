# 09 Positivity

To receive the flag you need create a python object that:

* Is no larger than 72 characters
* Must take parameters: obj = constructor(default)
* Must increment the passed parameter (++obj)

The source code (minus the flag) was provided.

## Write-up

The source code included comments with hints about operator overloading and
creating classes using the type() built-in.

One weakness of the test included in the source code was the way it checks your
class incremented correctly. To do that it will initialise it to a random value
between 0 and 100,000 and then use your classes increment method and compare
the result. It would be possible to create a class that doesn't do the
requested increment instead it simply returns a fixed value. Then you retry
until you get lucky and the service chooses the same initialisation value as
your fixed value. Assuming there are no rate limits on the testing server, you
could just keep trying, eventually it would be correct. At 1 second per test it
would take ~28 hours to try 100,000 requests which should hopefully be
sufficient. That is well within the time limit of the CTF so the player could
work on a different challenge while they waited. Also assuming the online
service matches the source code and is limited to 100,000 and not some larger
value.

I didn't go that route though.

I started with a basic class, this isn't mean to pass the all the requirements,
more of a starting point.

```
class Foo(object):
    def __init__(self, x):
        self.x = x

    def __pos__(self):
        self.x += 1
        return self.x


z = Foo(5000)
print('%s' % ++z)
print('%s' % ++z)
print('%s' % ++z)
```

Next, using the hint of using `type` built-in in the source code comments to
create the class, rather than using the more formal Class definition. I also
needed to work out how to handle the ++ operation and found that `__pos__`
provided this feature.

```
def xxxinit(self, x):
    self.x = x


def xxxpos(self):
    self.x += 1
    return self.x


# 72 characters:
# ----------------------------------------------------------------------
bar = type('Foo', (object,), {'__init__': xxxinit, '__pos__': xxxpos})

z = bar(5000)
print('%s' % ++z)
print('%s' % ++z)
print('%s' % ++z)
```

Next remove the type built-in, since all built-ins were rejected by the
service. I found I could replace this with `''.__class__.__class__` - The class
of a empty string is "str" and the class of a "str" is "type". Additionally,
the function declarations needed to go, so they were swapped out with lambdas.
After a few iterations I finally stumbled across something that worked and fit
within the 72 character limit.

```
# 72 characters:
# ----------------------------------------------------------------------
# bar = type('X', (), {'x': 0, '__init__': lambda s, x: s.__dict__['x'].__set__(x), '__pos__': lambda s: s.__dict__})
# bar = type('X', (), {'x': 0, '__init__': lambda s, x: None, '__pos__': lambda s: s.__dict__})
# bar = ''.__class__.__class__('X', (), {'x': 0, '__init__': lambda s, x: s.__setattr__('x', x), '__pos__': lambda s: s.__getattribute__('x') + 1})
# bar = ''.__class__.__class__('X', (0x0.__class__,), {'x': 0})
# bar = ''.__class__.__class__('X', (0x0.__class__,), {'__pos__': lambda x: x.__add__(1)})
bar = ''.__class__.__class__('X',(0x0.__class__,),{'__pos__':lambda x:x+1})

z = bar(5000)
print('%s' % dir(z))
print('%s' % z.__dict__)
print('%s' % z.real)
print('%s' % ++z)
print('%s' % ++z)
print('%s' % ++z)
```

Now we can submit and see the result... (note the challenge was internal and
the host mentioned below is no longer in service).

```
% nc 2015.ctf.captchaflag.com 9003

    Welcome to the Python positivity challenge!

    Create a type that, when instantiated, can be incremented with `++x`.

    Your input will be filtered in unusual ways, so please read the source!

    ''.__class__.__class__('X',(0x0.__class__,),{'__pos__':lambda x:x+1})
flag{thanks_for_staying_positive}
```
