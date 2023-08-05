# 18 Obvious once you see it

The answer should be obvious once you see it. Start here.

# Design

The link sends you to a HTML page with an image of the letters CX.

The image is created using SVG and the code for that is embedded into the HTML.

# Write-up
The challenge text implies something is not visible. The SVG has a lot of path
elements with their opacity set to 0. By editing the file to set these values
to 1 reveals some text under the CX letters:

CiscoOffersExternalPentestServices

The SVG has some obvious code at the end that is run when the page loads.

```SVG
<animate animate onbegin='
	var hiddenflagvalue="";
	var x=hex_sha1(document.getElementById("cxlogo").getElementById("d"),getAttribute("d") + hiddenflagvalue);
	if (x==="5396fbf4875c8897df0917d0e831dd9b4e796fad") {
		alert("You Found the Flag!");
	} else {
		alert("Keep Looking for the Flag!" + x);
	} ' attributeName=x dur=1s>
```

There is also the hex_sha1 function in JavaScript at the top of the page. I
will assume this is a standard implementation, not tampered with, and will
overlook it for now.

It seems like we need to find some string to put into the "hiddenflagvalue"
variable that when hashed matches "5396fbf4875c8897df0917d0e831dd9b4e796fad".

To make it slightly harder, the hiddenflagvalue is mixed with attribute "d" of
element "d" from the SVG. This can be found at the top of the SVG:

```SVG
<path id="d" opacity="0.94" fill-rule="evenodd" clip-rule="evenodd" fill="#1BBBEC" d="M162.8,0c88.8,1.2,118.9,56.1,122.6,68c3.2,10.3-3.3,25.3-10.4,31.9c-8.4,7.8-25.3,11.4-36.3,5.2
	c-15.3-8.6-28.6-36.4-74.5-36.9c-52.8-0.6-95.6,47-95.6,105c0,58,58.8,105.4,95.6,105c30.4-0.3,54.9-20.4,70.2-32.1c17.5-13.4,36.4-0.9,44.5,7.1c12.3,12.1,12.5,34.9-1,45.5c-19.5,15.4-46.7,47.5-115.1,48.3C72.9,347,0,269.3,0,173.5S72.9,0,162.8,0z"/>
```

Another "obvious when you see it" aspect is the use of a comma instead of a dot:

```SVG
var x=hex_sha1(document.getElementById("cxlogo").getElementById("d"),getAttribute("d") + hiddenflagvalue);

Should be:
var x=hex_sha1(document.getElementById("cxlogo").getElementById("d").getAttribute("d") + hiddenflagvalue);
                                                                ----^
```

The hash_sha1 function takes a single string, and with the comma it was always
passing the element "d" and ignoring the attribute "d" and the
"hiddenflagvalue".

Using the string "CiscoOffersExternalPentestServices" for the hiddenflagvalue
does not work. This is somewhat expected, the flag probably has to have flag{}
around it. Using "flag{CiscoOffersExternalPentestServices}" also fails.

There also seemed to be some other typo issues with the file. I extracted the
SVG code to a separate file, obvious.svg and tried to open it. This showed some
syntax errors. Easy fixes that were likely not important like attributes
without quotes, but also "<animate animate" this should just be "<animate" and
ending tag mismatch: ">" when it should be "/>".

I then opened the SVG file in Inkscape to see if there were any shapes drawn
out of bounds, perhaps not visible within the image canvas area. However, all
the elements appeared to be what could be seen.

I've been unable to get any further...
