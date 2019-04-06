import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Настройки отправки письма
FROM_ADDRESS = ''
TO_ADDRESS = ''
SUBJECT = 'Your MD5hash'
MESSAGE = ''
#Настройки SMTP сервера
SMTP_SERVER = 'smtp.gmail.com:587' #Пример: 'smtp.gmail.com:587'
LOGIN = ''
PASSWORD = ''

def sendemail(from_addr=FROM_ADDRESS, to_addr=TO_ADDRESS,
              subject=SUBJECT, message=MESSAGE,
              login=LOGIN, password=PASSWORD,
              smtpserver=SMTP_SERVER):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    mail = msg.as_string()
    server.sendmail(from_addr, to_addr, mail)
    server.quit()
