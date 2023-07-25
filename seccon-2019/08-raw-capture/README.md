# 08 Raw Capture

Our on-site team managed to do a raw capture of the wifi traffic at our target. They've sent it back to the "boys in the lab". Unfortunately for you, you're one of the "boys" in the lab. Get the file and see what you can do with it.


## Design

The challenge provides a 500K raw.cap file containing network traffic.

## Write-up

The raw.cap file can be opened in wireshark.

Browsing the packets I could see there seemed to be traffic between a raspberry pi and a tp-link device.

The first frame is the raspberry pi mentioning an SSID "secconctf".

The rest of the traffic does not seem readiliy readable and is presumably encrypted WIFI traffic.

The flag could be the wifi password, but more likely since there are so many packets it is in the content somewhere.

I have already completed a wifi cap cracking challenge in 2016 https://github.com/tobyoxborrow/ctf/tree/master/seccon-2016/08-wifipcap, so I can refer back to that.

I tried with the rockyou password list:

```Shell
aircrack-ng -w /usr/share/wordlists/rockyou.txt raw.cap


                              Aircrack-ng 1.5.2

      [00:16:08] 9598251/9822768 keys tested (9203.39 k/s)

      Time left: 0 seconds                                      97.71%

                                KEY NOT FOUND
```

After about 15 minutes of trying, the key was not found.

Next, try some of the wordlists in the SecLists project.

```Shell
aircrack-ng -w $(find ~/github.com/SecLists/Passwords -name "*.txt" | tr '\n' ',') raw.cap

                              Aircrack-ng 1.5.2


      [00:18:36] 12035105/12789845 keys tested (8766.17 k/s)

      Time left: 0 seconds                                      94.10%

                                KEY NOT FOUND
```

This also failed.

I next started to build a custom wordlist using some of the information available, such as:
* wifi
* secconctf, seccon, ctf
* raspberry, pi
* tplink, tp-link
* tplink default user/pass: admin

```Shell
root@kali# aircrack-ng -w words1.txt raw.cap

                              Aircrack-ng 1.5.2

                 10/9 keys tested

      Time left: 0 seconds                                     111.11%

                                KEY NOT FOUND
```

Still failed.

I also tried running my custom wordlist through John the Ripper to create variations with numbers and so on.

```Shell
john -stdout -wordlist:words1.txt -rules:KoreLogic  > john1.txt
Using default input encoding: UTF-8
Press 'q' or Ctrl-C to abort, almost any other key for status
112663173p 0:00:00:08 100.00% (2019-10-26 13:17) 12588Kp/s raspberrZ

aircrack-ng -w john1.txt raw.cap


                              Aircrack-ng 1.5.2

      [00:01:38] 1100800/110463130 keys tested (10834.03 k/s)

      Time left: 2 hours, 48 minutes, 14 seconds                 1.00%

                       Current passphrase: Tplink48865


      [07:03:20] 107230415/110463130 keys tested (3296.38 k/s)

      Time left: 0 seconds                                      97.07%

                                KEY NOT FOUND
```

This required many hours but also failed.

I continued, trying other lists in the SecLists project:
* Password lists
* Fuzzing list
* Usernames list

Next I wanted to use cewl to create a wordlist from the CTF page with the list of challenges. However, due to its use of JavaScript cewl didn't get anything useful.

So I manually copied the rendered HTML by running the following in the JavaScript console of the browser:

```Shell
copy(document.querySelector('html').innerHTML)
```

Save that to a file and ran a quick web server to host it:

```Shell
python3 -m http.server 80
```

Now I can use cewl to create a wordlist from the page:

```Shell
cewl localhost/problems.html --depth 0 > cewl.txt
```

I checked the output and cleaned it up, making it all lowercase and removing duplicates. It should be all lowercase as John will do the necessary transformations on it, including changing case.

Now feed it into John and perform some transformations.

```Shell
john -stdout -wordlist:cewl.txt --rules > john8.txt
john -stdout -wordlist:cewl.txt --rules=jumbo > john8jumbo.txt
john -stdout -wordlist:cewl.txt --rules=Try > john8Try.txt
john -stdout -wordlist:cewl.txt --rules=TryHarder > john8TryHarder.txt
```

Still not found.

I tried again using cewl, but this time with all the pages on the CTF site and running them through John.

```
aircrack-ng -w ./johnE.txt raw.cap

                              Aircrack-ng 1.5.2

      [00:00:11] 99543/636103 keys tested (7494.84 k/s)

      Time left: 1 minute, 11 seconds                           15.65%

                           KEY FOUND! [ SeCcOnCtF ]
```

Finally. And frustratingly simple.

With the key, I could use Wireshark to decrypt all the traffic following the steps on https://wiki.wireshark.org/HowToDecrypt802.11

The capture included a lot of noise, so I filtered various packets out:
```
!(wlan.fc.type_subtype == 0x0018) and !(wlan.fc.type_subtype == 0x001a) and !(wlan.fc.type_subtype == 0x0005) and !(wlan.fc.type_subtype == 0x001d) and !(wlan.fc.type_subtype == 0x0019) and !(wlan.fc.type_subtype == 0x001b) and !(wlan.fc.type_subtype == 0x001c)
```

After scrolling 55 packets, I come across a DHCP request:

```
0000   aa aa 03 00 00 00 08 00 45 00 01 90 d0 9f 00 00   ........E.......
0010   40 11 a8 be 00 00 00 00 ff ff ff ff 00 44 00 43   @............D.C
0020   01 7c 81 33 01 01 06 00 15 1e 7a a8 00 00 00 00   .|.3......z.....
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0040   dc a6 32 0e 72 c0 00 00 00 00 00 00 00 00 00 00   ..2.r...........
0050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0060   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0070   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0080   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0090   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00a0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00b0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00c0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00d0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00e0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00f0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0100   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0110   63 82 53 63 35 01 03 3d 07 01 dc a6 32 0e 72 c0   c.Sc5..=....2.r.
0120   32 04 c0 a8 00 39 39 02 05 c0 3c 2e 64 68 63 70   2....99...<.dhcp
0130   63 64 2d 37 2e 30 2e 38 3a 4c 69 6e 75 78 2d 34   cd-7.0.8:Linux-4
0140   2e 31 39 2e 36 36 2d 76 37 6c 2b 3a 61 72 6d 76   .19.66-v7l+:armv
0150   37 6c 3a 42 43 4d 32 38 33 35 0c 28 66 6c 61 67   7l:BCM2835.(flag
0160   7b 64 61 74 61 5f 63 61 6e 5f 6c 65 61 6b 5f 69   {data_can_leak_i
0170   6e 5f 74 68 65 5f 6f 64 64 65 73 74 5f 70 6c 61   n_the_oddest_pla
0180   63 65 73 7d 91 01 01 37 0e 01 79 21 03 06 0c 0f   ces}...7..y!....
0190   1a 1c 33 36 3a 3b 77 ff                           ..36:;w.
```

flag{data_can_leak_in_the_oddest_places}
