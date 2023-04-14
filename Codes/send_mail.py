
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
from email.mime.image import MIMEImage

def mail(length, lengthp, img):

    with open(img, 'rb') as f:
        img_data = f.read()

    configur = ConfigParser()
    configur.read('configurations.ini')

    msg = MIMEMultipart()

    msg['Subject'] = 'Test mail with attachment'
    msg['From'] = configur.get('SMTPlogin', 'sender_address')
    msg['To'] = configur.get('SMTPlogin', 'receiver_address')

    text = "Length of Key: {}; Length of Private Key: {}".format(str(length), str(lengthp))

    msg.attach(MIMEText(text, "plain"))

    image = MIMEImage(img_data, name=basename(img))
    msg.attach(image)

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(configur.get('SMTPlogin', 'mailtrap_user'), configur.get('SMTPlogin', 'mailtrap_password'))
        server.sendmail(configur.get('SMTPlogin', 'sender_address'), configur.get('SMTPlogin', 'receiver_address'), msg.as_string())
        print("Successfully sent email")