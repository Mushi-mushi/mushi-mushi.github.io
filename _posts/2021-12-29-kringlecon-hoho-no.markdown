---
layout: post
title:  "A new foe has appeared !"
date:   09-02-2020 13:34:34
categories: malware
tags: kringlecon
---
Introduction
------------
It's this time of the year again ! The SANS xmas challenge is back and I though I would documented some of the challenges as a way to get back into this blog. Without further ado, let's jump into it !
Ho Ho ...No !
--------------
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
{% endhighlight %}
