---
layout: default
title: Generating the best payloads
---


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
![](https://mushi-mushi.github.io/ressources/veil/veil-menu.png){: height="36px" width="36px"}
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
apt -y install veil
/usr/share/veil/config/setup.sh --force --silent
{% endhighlight %}
