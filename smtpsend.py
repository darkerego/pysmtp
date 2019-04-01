# Darkerego, April 2019
# Send Mail
from conf import *  # <--- Configure first !
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import time
import sqlite3
import uuid
import re
from random import randint
# Tracking functions


def bootstrap_db():
    global db
    db.execute("CREATE TABLE IF NOT EXISTS targets(email_address, uuid)")
    db.commit()


def save_tracking_uuid(email_address, target_uuid):
    global db
    db.execute("INSERT INTO targets(email_address, uuid) VALUES (?, ?)", (email_address, target_uuid))
    db.commit()


def create_tracking_uuid(email_address):
    tracking_uuid = str(uuid.uuid4())
    save_tracking_uuid(email_address, tracking_uuid)
    return tracking_uuid


def inject_tracking_uuid(email_text, tracking_uuid):
    TRACK_PATTERN = "\[TRACK\]"
    print("Injecting tracking UUID %s" % tracking_uuid)
    altered_email_text = re.sub(TRACK_PATTERN, tracking_uuid, email_text)
    return altered_email_text


def delay_send():
    sleep_time = randint(1, 55) + (60*5)
    time.sleep(sleep_time)


def get_file_email(email_filename):
    email_text = ""
    try:
        with open(email_filename, "r") as infile:
            print("Reading " + email_filename + " as email file")
            email_text = infile.read()
    except IOError:
        print("Could not open file " + email_filename)
        exit(1)

    return email_text


def send(email_filename):
    global db
    if track:
        if db_name is not None:
            db = sqlite3.connect(db_name)
            bootstrap_db()
        else:
            print("Error: DB name is empty")
            exit(1)

    email_text = ""

    try:
        email_text = get_file_email(email_filename)
    except TypeError:
        print("Error: Could not load email from file %s" % email_filename)
        exit(1)

    to_addresses = []
    if receiver_email is not None:
        to_addresses.append(receiver_email)

    else:
        print("Error: Could not load input file names")
        exit(1)

    try:
        print("Connecting to SMTP server at " + smtp_server + ":" + str(port))
        server = smtplib.SMTP(smtp_server, port)
        if tls:
            server.starttls()
        if use_auth:
            print('Attempting Authentication...')
            try:
                server.login(username, password)
            except Exception as err:
                print('Error authenticating: ' + str(err))
                exit(1)
        msg = MIMEMultipart("alternative")
        msg.set_charset("utf-8")

        if from_name is not None:
            print("Setting From header to: " + from_name + "<" + sender_email + ">")
            msg["From"] = from_name + "<" + sender_email + ">"
        else:
            print("Setting From header to: " + sender_email)
            msg["From"] = sender_email

        if reply_to is not None:
            print("Setting Reply-to header to " + reply_to)
            msg["Reply-to"] = reply_to

        if subject is not None:
            print("Setting Subject header to: " + subject)
            msg["Subject"] = subject

        if important:
            msg['X-Priority'] = '2'

        if image:
            with open(image, "rb") as imagefile:
                img = MIMEImage(imagefile.read())
                msg.attach(img)

        for to_address in to_addresses:
            msg["To"] = to_address

            if track:
                tracking_uuid = create_tracking_uuid(to_address)
                altered_email_text = inject_tracking_uuid(email_text, tracking_uuid)
                msg.attach(MIMEText(altered_email_text, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(email_text, 'html', 'utf-8'))

            if attachment_filename is not None:

                ctype, encoding = mimetypes.guess_type(attachment_filename)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(attachment_filename, "rb") as attachment_file:
                    inner = MIMEBase(maintype, subtype)
                    inner.set_payload(attachment_file.read())
                    encoders.encode_base64(inner)
                inner.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
                msg.attach(inner)

            server.sendmail(sender_email, to_address, msg.as_string())
            print("Email Sent to " + to_address)
            if slow_send:
                delay_send()
                print("Connecting to SMTP server at " + smtp_server + ":" + str(port))
                server = smtplib.SMTP(smtp_server, port)
                server.sendmail(sender_email, to_address, msg.as_string())

    except smtplib.SMTPException as err:
        print("Error: Could not send email")
        raise err
