import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from datetime import datetime

def reports_Mail():

    now = datetime.now()
    now = [now.month,now.day,now.year]
    now = str(now)

    from_addr = "FROM ADDRESS"
    to_addr = "TO ADDRESS"

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = ("SUBJECT FIELD : "+now)

    body = " BODY FIELD "

    msg.attach(MIMEText(body, 'plain'))

    filename = " FILENAME "
    attachment = open(" LINK TO ATTACHMENT ", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP(" SMTP ADDRESS ", SMTP PORT)
    server.starttls()
    server.login(" MAIL SERVER USERNAME ", " MAIL SERVER PASSWORD")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

