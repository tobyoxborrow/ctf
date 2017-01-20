# 01 Clicks

The flag is stored on a web page. It will be revealed after clicking the page
enough times.

## Write-up

When you click the page some JavaScript event triggers and attempts to decrypt
the flag with a decryption key that is initialised at 0. It displays the result
and then increments the decryption key. The next time you click it is trying a
different decryption key and would increment every time you try.

Since the HTML and JavaScript were provided, I decided to take the files and
store them locally. Then add a function that would call the decrypt function
directly without any clicking needed. It would run from 0 to some very large
number and stop when it found the string "flag", then display the result.

```
function tryDecrypt() {
    var is_found = Boolean(false);
    console.log('starting...');
    for (var c = 0; c < 900000000; c++) {
        var result = decrypt(c);
        if (result.indexOf('flag') >= 0) {
            console.log(c);
            console.log(result);
            is_found = true;
            alert('Found!');
            alert(result);
            break;
        }
    }
    if (! is_found) {
        alert('Not found');
    }
}
```

Just to make it user-friendly, this was tied to a button on the page. Then I
just had to load the page locally in a browser, click the button and wait.

```
<body>
<button onclick="tryDecrypt()">Decrypt</button>
</body>
```

In the JavaScript console log the result could be seen shortly after starting:

```
[Log] starting... (clicks.html, line 20)
[Log] 1049 (clicks.html, line 25)
[Log] flag{xrain_xor_xshine} (clicks.html, line 26)
```
