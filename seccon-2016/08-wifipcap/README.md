# 08 WIFI PCAP

The flag is stored on flag.html of a web-server. You have a pcap file of WIFI
traffic of someone accessing that page.

## Write-up

Since the WIFI traffic is encrypted with standard WIFI encryption first we need
to break that before we can read the packets in the file. Fortunately around
the time of the CTF I attended a tutorial at Cisco SecCon that introduced
cracking WIFI. As such I knew I needed aircrack-ng and a wordlist.

I used the rockyou.txt wordlist as it is fairly large and successful. Within a
second, the forth word in the list, the password was found. It was just
"password".

```
% aircrack-ng -w ./rockyou.txt network-wifi-capture.cap


                                 Aircrack-ng 1.2 rc4

      [00:00:00] 4/7120714 keys tested (605.88 k/s)

      Time left: 3 hours, 16 minutes, 9 seconds                  0.00%

                           KEY FOUND! [ password ]


      Master Key     : EE ED E0 CC A3 0E 16 EF A7 0B 7C A8 62 A7 D4 BD
                       89 52 1D 97 32 7E 89 CC 33 FF 89 BE AD 8F 52 9A

      Transient Key  : 0F 08 8F E3 F7 87 C2 B0 52 BA C6 8F 52 1A AB 6D
                       BC F1 18 87 9D C2 19 F2 AA 7D A8 16 9C E8 83 8E
                       12 0F 11 86 96 C6 E7 26 23 95 2D 9A B2 DF E8 F0
                       74 27 AF FB 11 B5 FC 59 13 61 D8 FE DE 1D A5 ED

      EAPOL HMAC     : B1 07 87 3C 1B B3 3F 16 95 94 BD A8 F4 2A DA C2
```

Then it was just a matter of opening the capture in Wireshark, providing it the
password and you can view the packets. There was not much to look through, and
you can quickly find the HTTP request for flag.html and the response from the
server containing the key: flag{Wifi_Attacks_Are_Fun}.
