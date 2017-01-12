# 05 Hidden

The flag is stored in the JavaScript code of a website. The JavaScript code has
been obfuscated.

## Write-up

Viewing the source code and trying to work it out by manually reading it wasn't
really an option.

I found an extension for Firefox that would "deobfuscate" JavaScript.

[JavaScript Deobfuscator](https://addons.mozilla.org/en-us/firefox/addon/javascript-deobfuscator/)

After installing that and reloading the webpage the flag was easily visible in
the addon's window.

```
sessionStorage.flag = 'flag{not_a_good_hiding_place}'
```
