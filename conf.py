port = 25  # For SSL
smtp_server = "smtp.sendgrid.net"
sender_email = "admin@localhost"  # Enter your address
receiver_email = "somebody@protonmail.com"  # Enter receiver address
username = 'apikey'
password = 'yourpasswordhere'
tls = False  # Authenticate to mail relay with tls
DEBUG = False  # debug mode
use_auth = True  # mailserver require authentication
# Mail Headers
from_name = 'Admin'  # Sender's Name
reply_to = None  # Optional : set reply-to headers
subject = 'Send Email With Python'  # outgoing email subject
important = False  # x-priority
image = False  # attach an image
track = False  # track message with a uuid
attachment_filename = None  # attach a file to message
slow_send = False  # delay sending
db_name = 'database'  # uuid db (optional)
email_filename = 'test.msg'  # don't change

