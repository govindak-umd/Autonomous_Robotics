import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
command = 'raspistill -w 1280 -h 720 -vf -hf -o ' + pic_time + '.jpg'
os.system(command)

#EMAIL
smtpUser = 'enpm809tslamdunk@gmail.com'
smtpPass = 'pi@slamdunk'

#DESTINATION
toAdd = 'govindajithkumar97@gmail.com'
fromAdd = smtpUser
subject = 'IMAGE RECORDED FROM PI' + pic_time
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = fromAdd
msg['To'] = toAdd
msg.preamble = "IMage recorded at : " + pic_time

#EMAIL TEXT
body = MIMEText("Image recorded at : " + pic_time)
msg.attach(body)

fp = open('sonartestimage'+'.jpg','rb')
img = MIMEImage(fp.read())
fp.close()
msg.attach(img)

#send email

s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser,smtpPass)
s.sendmail(fromAdd, toAdd, msg.as_string())
s.quit()

print("Email DELIVERED!!!!!")