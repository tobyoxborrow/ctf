# 20 clean_docs

We let the intern finalize the yearly report, however unfortunantly they also
redacted some data we needed! Can you please recover the flag for us?

You can find the report here. Many thanks.

# Design

The challenge provided a 104 page annual report PDF file. The annual report was
for a real amusement park. The document has some black boxes covering up some
words.

Also the PDF had some copy-protection enabled. So even though you can highlight
text, you can not copy it to the clipboard. You required a password to disable
this.

# Write-up
Redaction is just some black boxes above the actual words which are still there.

The file had copy-protection, but it was trivially easy to remove (and perhaps
other PDF viewers won't even implement it). I opened the PDF in macOS Preview,
the default PDF viewer, and exported the file to a new PDF. This new PDF was
the same file, but had no copy-protection. I could now copy the text behind the
black boxes and paste it somewhere else to view.

The only challenge is there are a lot of black boxes so you don't know exactly
which one the flag is behind...

Select All. Copy. Paste into text file. Search for "flag{". Done.

```
... value of the asset or group of assets may not be recoverable.
Flag{Red4ct0n_i5_h4rd!}. Recoverability of assets to be held and used ...
```
