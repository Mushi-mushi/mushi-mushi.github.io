---
layout: post
title:  "Kringlecon 2021 - Ho Ho ...No !"
date:   29-12-2021 13:34:34
categories: exploitation
tags: kringlecon
---

It's this time of the year again ! The SANS xmas challenge is back and I though I would documented some of the challenges as a way to get back into this blog. Without further ado, let's jump into it !

Ho Ho ...No !
-------------
This challenge is focused on the famous fail2ban. Here is the challenge:
{% highlight bash%}
Jack is trying to break into Santa's workshop!

Santa's elves are working 24/7 to manually look through logs, identify the
malicious IP addresses, and block them. We need your help to automate this so
the elves can get back to making presents!

Can you configure Fail2Ban to detect and block the bad IPs?

 * You must monitor for new log entries in /var/log/hohono.log
 * If an IP generates 10 or more failure messages within an hour then it must
   be added to the naughty list by running naughtylist add <ip>
        /root/naughtylist add 12.34.56.78
 * You can also remove an IP with naughtylist del <ip>
        /root/naughtylist del 12.34.56.78
 * You can check which IPs are currently on the naughty list by running
        /root/naughtylist list

You'll be rewarded if you correctly identify all the malicious IPs with a
Fail2Ban filter in /etc/fail2ban/filter.d, an action to ban and unban in
/etc/fail2ban/action.d, and a custom jail in /etc/fail2ban/jail.d. Don't
add any nice IPs to the naughty list!
   
*** IMPORTANT NOTE! ***

Fail2Ban won't rescan any logs it has already seen. That means it won't
automatically process the log file each time you make changes to the Fail2Ban
config. When needed, run /root/naughtylist list refresh to re-sample the log file
and tell Fail2Ban to reprocess it.
{% endhighlight %}

To resolve this challenge, [fail2ban-client][link1] will be rather helpful, as well as [fail2ban-regex][link2]

Fail2Ban jail "kinglecon"
----------------------------
The config requirement for this file are:
   - log entries in /var/log/hohono.log
   - 10 or more failure messages
   - within an hour

Which gives us something like this:
{% highlight bash%}
[kringlecon]
findtime = 3600
bantime = 600
maxretry = 10
backend = auto
filter   = kringle
banaction = kringle
enabled = true
logpath  = /var/log/hohono.log
{% endhighlight %}
Obviously the filter and banaction "kringle" still need to be defined at this point


Fail2Ban action "kinglecon"
-----------------------------
This one is very straightforward, let's not forget to put the full path of the naughtylist executable and we should be good to go:
{% highlight bash%}
[Definition]
actionban = /root/naughtylist add <ip>
actionunban = /root/naughtylist del <ip>
{% endhighlight %}
Finally, we need to set up our filter.

Fail2Ban filter "kinglecon"
-----------------------------
 Grepping the log file for different kind of log shows four interesting type of log:
{% highlight bash%}
[Definition]
failregex  = ^.* Login from <HOST> rejected due to unknown user name.*$
             ^.* Failed login from <HOST> for .*$
             ^.* <HOST> sent a malformed request.*$
             ^.* Invalid heartbeat .* from <HOST>.*$
{% endhighlight %}
Be carefull that the timestamps are automatically processed while using fail2ban-regex but not in the filter (or the other way around...)
   
[link1]:https://www.fail2ban.org/wiki/index.php/Commands 
[link2]:https://fail2ban.readthedocs.io/en/latest/filters.html
