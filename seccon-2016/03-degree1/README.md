# 03 Degree 1

The flag is stored in an online API.

A pcap is provided which contains examples of someone using the API.

## Write-up

The pcap reveals the service is a typical HTTP restful API of some kind of
university students database.

Within it there are a few types of requests
* GET /students
* GET /students/ID
* GET /advisors/ID

The response body is in JSON.

Example request and response:
```
GET /advisors/580539765512aa0024590f02 HTTP/1.1
Host: 192.168.99.101:9022
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8
Cookie: flask=eyJ0aWQiOiJGN0pYNjZBQ0RYVFpHS1pMRDRSMktZM0JXIn0.CubB2A.TvA2CTgQ0euEAF0GudVrdJ3Ldis; JSESSIONID=399CE6D3BCC0F4064AEC2E4A90011465

HTTP/1.1 200
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Date: Mon, 17 Oct 2016 21:04:56 GMT

a7
{"id":"580539765512aa0024590f02","firstName":"Lou","lastName":"Reed","degrees":[{"awarded":"1958-03-02","philosophia":"Vocals","school":"The Factory","advisor":null}]}
0
```

I decided to write a crawler that starts at /students/ and requests each
student and each of their advisors. We don't know what we are looking for,
though hopefully it is in the format "flag{...}". Rather than make the script
stop when it saw this I just let it grab everything then I could manually
review it.

The crawler script is included here.

I do not have an example of it finding the flag but the flag as I remember was
stored in one of the attributes of one of the advisors.
