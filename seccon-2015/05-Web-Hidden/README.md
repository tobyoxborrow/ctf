# 05 Hidden

The flag is stored in the javascript code of a website. The javascript code has
been obfuscated.

## Write-up

Viewing the source code and trying to work it out by manually reading it wasn't
really an option.

I found an extension for firefox that would "deobfuscate" javascript.

[JavaScript Deobfuscator](https://addons.mozilla.org/en-us/firefox/addon/javascript-deobfuscator/)

After installing that and reloading the webpage the flag was easily visible in
the addon's window.

```
sessionStorage.flag = 'flag{not_a_good_hiding_place}'
```
