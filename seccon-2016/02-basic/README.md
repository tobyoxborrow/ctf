# 02 Brute

The flag is stored in an online service that is protected by a username and
password.

A pcap is provided which contains brute force attempts to login to a web
service.

## Write-up

The pcap contains 48,000 packets. We are only interested in those requests that
had a successful reply from the server, so filter for that.

```
http.response.code == 200
```

One packet matches.

Right-click, Follow -> HTTP Stream

```
GET / HTTP/1.1
Host: 192.168.99.100:9000
Authorization: Basic YWRtaW46TWVsbG9u
User-Agent: curl/7.43.0
Accept: */*

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/0.11.11 Python/2.7.12
Date: Fri, 23 Sep 2016 18:55:23 GMT

Hello World!
```

The basic authorization string can be easily decoded:

```
% echo "YWRtaW46TWVsbG9u" | base64 --decode
admin:Mellon
```

We can use these credentials to login to the service and retrieve the flag.
