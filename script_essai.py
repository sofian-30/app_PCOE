import email, smtplib, ssl

from email import encoders

from email.mime.base import MIMEBase

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.message import EmailMessage

from email.mime.application import MIMEApplication

import mimetypes

from datetime import date

 

 

EMAIL_ADDRESS = 'no-reply@seenovate.com'

EMAIL_PASSWORD = 'S33nov@te001!'

RECIPIENTS = ['remy.fouchereau@seenovate.com']

CC = ['sofian.ouass@seenovate.com']

CC = ['']

ATTACHMENTS = ['CA_2023.xlsx']

subject = 'Tests'

 

body = "Bonjour, \n\nVoici le test du jour. \n\nCordialement, \nSeenovate"

 

msg = EmailMessage()

msg['Subject'] = subject

msg['From'] = EMAIL_ADDRESS

msg['To'] = ",".join(RECIPIENTS)

msg['Cc'] = ",".join(CC)

msg.set_content(body)

 

#today = date.today().strftime('%Y%m%d')

#for file in ATTACHMENTS:

#    filename = file

#    # path = './diffusion/' + filename

#    ctype, encoding = mimetypes.guess_type(filename)

#    if ctype is None or encoding is not None:

#        ctype = 'application/octet-stream'

#    maintype, subtype = ctype.split('/', 1)

#    with open(filename, 'rb') as fp:

#        msg.add_attachment(fp.read(),

#                        maintype=maintype,

#                        subtype=subtype,

#                        filename=filename)

 

 

context = ssl.create_default_context()

 

with smtplib.SMTP(host ='pro2.mail.ovh.net', port = 587) as smtp:

    smtp.starttls(context = context)

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)