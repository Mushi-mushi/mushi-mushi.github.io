---
layout: default
title: Cheatsheet
---

Upgrading Simple Shells to Fully Interactive TTYs
--------------
{% highlight bash%}
python -c 'import pty; pty.spawn("/bin/bash")'
{% endhighlight %}

Then press CTRL+Z to background

{% highlight bash%}
stty raw -echo
{% endhighlight %}

Press Enter, fg, then Enter twice to return to your original shell

{% highlight bash%}
stty -a
{% endhighlight %}

This will give you the number of columns and rows of the terminal

{% highlight bash%}
stty rows number_of_row columns number_of_columns
{% endhighlight %}

Interesting Links:
--------------
- https://jwt.io/                     Decode and edit jwt token
- https://gchq.github.io/CyberChef/   Decode and encode in multiple format
- https://stackedit.io/app#           Markdown editor
- https://devhints.io/jekyll          Jekyll dev ops tricks
- https://jekyllrb.com/               Jekyll tuto
- https://github.com/swisskyrepo/PayloadsAllTheThings   Payload for everything
