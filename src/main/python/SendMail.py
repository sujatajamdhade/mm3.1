import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys

COMMASPACE = ', '


class SendMail:
    def __init__(self, sender='', password='', recipients=[], subject='', attachments=[], msg=''):
        self.sender = sender
        self.password = password
        self.recipients = recipients
        self.subject = subject
        self.attachments = attachments
        self.msg = msg

    def send(self):
        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = self.subject
        outer['To'] = COMMASPACE.join(self.recipients)
        outer['From'] = self.sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        # List of attachments
        if self.msg != None:
            text = self.msg
            outer.attach(MIMEText(text, 'plain'))  # or 'html'

        # Add the attachments to the message
        for file in self.attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.sender, self.password)
                s.sendmail(self.sender, self.recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise