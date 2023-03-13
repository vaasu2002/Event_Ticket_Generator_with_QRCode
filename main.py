import pandas as pd
from fpdf import FPDF
import pyqrcode
import png
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

df = pd.read_excel('payment_links_excel.xlsx')
tickets = df.to_dict(orient='records')

for ticket in tickets:
    pdfGen = {'name': ticket['full_name'], 'event': ticket['payment button title'],
              'venue': 'Where ever you find space', 'role': 'ATTENDEE',
              'date_time_event': '28 February 2023, 4PM to 7PM', 'order_no': ticket['order_id'],
              'payment_status': ticket['payment status'], 'email_id': ticket['email']}

    PAYMENT_STATUS = ""

    if pdfGen['payment_status'] == 'captured':
        PAYMENT_STATUS = "PAID"

    else:
        PAYMENT_STATUS = "UNPAID"

    EVENT_NAME = pdfGen['event']
    DATE_TIME_EVENT = pdfGen['date_time_event']
    VENUE_EVENT = pdfGen['venue']
    PER_NAME = pdfGen['name']
    ROLE = pdfGen['role']
    ORDER_NO = pdfGen['order_no']
    EMAIL_ID = pdfGen['email_id']

    if PAYMENT_STATUS == 'PAID':
        # Class for creating tickets
        class PDF(FPDF):

            def header(self):
                # Logo
                self.image('Event_Logo.png', 10, 8, 33)
                # Arial bold 15
                self.set_font('Arial', 'B', 15)
                # Move to the right
                self.cell(80)
                # Title
                self.cell(30, 10, 'Entry Pass')
                # Line break
                self.ln(20)

            def heading(self, EVENT_NAME):
                self.cell(80)
                # Font
                self.set_font("Arial", 'B', 40)
                # Event name
                self.cell(30, 30, EVENT_NAME, 0, 0, 'C')

            def date_time_venue(self, DATE_TIME_EVENT, VENUE_EVENT):
                self.cell(40)
                # Font
                self.set_font("Arial", 'B', 10)
                # DATE_TIME_VENUE
                self.cell(-110, 76, DATE_TIME_EVENT, 0, 0, 'C')
                self.cell(110, 88, VENUE_EVENT, 0, 0, 'C')

            def attendee_name(self, PER_NAME):
                self.set_y(70)
                self.set_font("Arial", 'B', 25)
                # ATTENDEE NAME
                self.cell(60, 50, PER_NAME, 0, 0, 'L')
                # self.cell(65, 58, ROLE, 0, 0, 'C')

            def role_in_event(self, ROLE):
                self.set_y(76)
                self.set_font("Arial", 'I', 10)
                # Role in Event
                self.cell(60, 52, f"ROLE: {ROLE}", 0, 0, 'L')

            def payment_status(self, PAYMENT):
                self.set_y(-37)
                self.set_font("Arial", '', 10)
                # Payment Status
                self.cell(0, 10, PAYMENT_STATUS, 0, 0, 'L')

            def order_number(self, order_no):
                self.set_x(-75)
                self.set_font("Arial", '', 10)
                # Order Number
                self.cell(0, 10, f"Order Number: {ORDER_NO}", 0, 0, 'L')

            def qr_code(self):
                # QR_CODE
                url = pyqrcode.create(ORDER_NO)
                url.png(f"{PER_NAME}_ticket.png", scale=6)
                self.image(name=f"{PER_NAME}_ticket.png", x=155, y=85, w=25, h=25)

            # Page footer
            def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-15)
                # Arial italic 8
                self.set_font('Arial', 'I', 8)
                # Page number
                self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


        pdf = PDF(format='A5', orientation='L')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.heading(EVENT_NAME=EVENT_NAME)
        pdf.date_time_venue(DATE_TIME_EVENT=DATE_TIME_EVENT, VENUE_EVENT=VENUE_EVENT)
        pdf.attendee_name(PER_NAME=PER_NAME)
        pdf.role_in_event(ROLE=ROLE)
        pdf.payment_status(PAYMENT=PAYMENT_STATUS)
        pdf.order_number(order_no=ORDER_NO)
        pdf.qr_code()
        pdf.output(f"{PER_NAME}_ticket.pdf", 'F')

        # Login credentials
        gmail_user = 'event.vitb@gmail.com'
        gmail_password = 'ENTER_PASSWORD_HERE'

        # Create a message container
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = EMAIL_ID
        msg['Subject'] = 'Event Ticket'

        # Add text to the email body
        text = MIMEText(f"Hey {PER_NAME},"
                        "\n PFA of your event Ticket"
                        "\n We hope you enjoy the event!")
        msg.attach(text)

        # # Add an image attachment to the email
        # with open('image.jpg', 'rb') as f:
        #     img = MIMEImage(f.read())
        #     msg.attach(img)

        # Add a pdf attachment to the email
        fileName = f"{PER_NAME}_ticket.pdf"
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

    else:
        print(PER_NAME)
