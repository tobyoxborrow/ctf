# 02 Expand the Flag

Say hello, tell me your name. I bet you can't eXpand My fLag TXT

The challenge link goes to a simple web form that asks for your name, two text input fields for your first and last name, and a button to submit.

## Write-up

The letters XML were capitalized in the challenge introduction. Also the name of the challenge includes Expand. XML Entity Expansion is a type of vulnerability and likely what's needed to get the flag.

https://en.wikipedia.org/wiki/XML_external_entity_attack

Entering text into the input boxes and submitting will load another page repeating the text back.

!(input.png)

!(output.png)

Some tests on the input fields:
* using the < character - the second page instead displays the message "Parsing Failed".
* using the HTML entity &quot; - the second page does not render it.
* using <![CDATA[x]]> - the second page just renders the contents and not the XML itself.

This is a good indicator the server is parsing the input as XML.

The HTML page for the input forms has a javascript function that runs when the submit button is clicked. The function takes the two input fields, wraps them up in tags and submits that new joined value rather than the two fields separately.

So "a" and "b" are wrapped up like:

```XML
<name>
<first_name>a</first_name>
<last_name>b</last_name>
</name>
```

If the server recieves data that doesn't quite match the format shown above, it will display an error message containing that data. For example, if the data just contains the name element and a CDATA block:

```XML
<name><![CDATA[foo]]></name>
```

The server parses the XML and displays the CDATA contents:

```Text
Hello  .
Unexpected data
name: foo
please contact to the development team.
```

We can potentially use this error message to have the server share with us information it should not.

Also worth noting there isn't any server side input sanitisation going on, which makes the attack much easier and more likely to pull off.

At this point it is assumed there is a file on the server with the flag we need to read and will use the XML entity expansion attack to read it. If that is true, as an extra challenge we also need to find the file, it isn't necessarily in the same directory as the script we are attacking.

To test faster, rather than trying via a web browser, I switched to Burp Suite's Repeater. I could submit directly to the server and skip the formatting automatically added by the javascript too.

!(burp.png)

The general idea for the XML Entity Expansion attack to be used here would be to define an entity, using any name we like, that points to a file on the server. Then reference that entity name, which will cause the server to expand the entity into the contents of the file.

Trying just simple entity expansion by having it expand to a known value:

```
data=<!DOCTYPE foo [ <!ENTITY bar "baz"> ]><name>&bar;</name>
```

This didn't work, the & and ; needed to be escaped:

```
data=<!DOCTYPE foo [ <!ENTITY bar "baz"> ]><name>%26bar%3b</name>
```

That worked as expected, the page displayed "name: baz".

Now we can try the file expansion.

Since we don't know the path to the flag file, we can start with some files with well-known paths, such as /etc/passwd.

```
data=<!DOCTYPE name [ <!ENTITY txt SYSTEM "file:////etc/passwd" > ]><name>%26txt;</name>
```

This returned the file, besides the standard users, there was a challenge user at the end:

```HTML
<pre>Hello  .
Unnexpected data
name: root:x:0:0:root:/root:/bin/bash
name: daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
[...]
name: challenge:x:999:999::/home/challenge:/bin/sh
```

We still don't know where the flag file is, but perhaps it is in their home directory?

```
data=<!DOCTYPE name [ <!ENTITY txt SYSTEM "file://///home/challenge/flag.txt" > ]><name>%26txt;</name>
```

And it was!
