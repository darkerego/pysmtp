# pysmtp
Library for sending emails via smtp in python

#### Usage


<pre>
python3

>>> from smtpsend import send
>>> send('message.html')
Reading test.msg as email file
Connecting to SMTP server at smtp.sendgrid.net:25
Attempting Authentication...
Setting From header to: Admin<admin@localhost>
Setting Subject header to: Send Email With Python!
Email Sent to somebody@protonmail.com
>>>

</pre>

