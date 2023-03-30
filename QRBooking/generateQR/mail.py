from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
gmail_user = 'Event.vitb@gmail.com'
gmail_password = 'jydbwqtbfvwwrdpv'

def send_ticket(email,full_name,registration_number,event_name,pdf_dir):
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = email
        msg['Subject'] = 'Event Ticket'
        # Add text to the email body
        text = MIMEText(f"Hey {full_name},"
                        f"\n PFA of your event {event_name} Ticket"
                        f"\n We hope you enjoy the event!")
        msg.attach(text)
        # # Add an image attachment to the email
        # with open('image.jpg', 'rb') as f:
        #     img = MIMEImage(f.read())
        #     msg.attach(img)
        # Add a pdf attachment to the email
        fileName = pdf_dir
        with open(fileName, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype='pdf')
        pdf.add_header('content-disposition', 'attachment', filename=os.path.basename(fileName))
        msg.attach(pdf)
        # Create the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()

    except:
        print(f"{registration_number}-{full_name} Failed to send mail")