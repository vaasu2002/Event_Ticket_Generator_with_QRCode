import pandas as pd
import qrcode
import pandas as pd
from fpdf import FPDF
import pyqrcode
import png
import os
import smtplib

class PDF(FPDF):
    def __init__(self,event_img_filepath:str):
        super().__init__(format='A5',orientation='L')
        self.event_img_filepath = event_img_filepath

    def header(self):
        # Logo
        self.image(self.event_img_filepath, 10, 8, 33)
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
        self.cell(0, 10, PAYMENT, 0, 0, 'L')
    def order_number(self, order_no):
        self.set_x(-75)
        self.set_font("Arial", '', 10)
        # Order Number
        self.cell(0, 10, f"Order Number: {order_no}", 0, 0, 'L')
    def get_qr_code(self,file_path:str):
        self.image(name=file_path, x=155, y=85, w=25, h=25)
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')




df = pd.read_excel("artifact/payment_data/payment_links_excel.xlsx")
confirm_payment_df = df[df['payment status']=='captured']
failed_payment_df = df[df['payment status']=='failed']

for index in range(0,len(confirm_payment_df)):
    try:

        registration_number = confirm_payment_df['registration_number'].iloc[index].upper()
        unique_id = confirm_payment_df['order_id'].iloc[index]
        event_name = confirm_payment_df['payment button title'].iloc[index]
        email = confirm_payment_df['email'].iloc[index]
        full_name = confirm_payment_df['full_name'].iloc[index].upper()
        gender = confirm_payment_df['gender'].iloc[index].upper()
        role = "ATTENDEE",
        payment_status = "PAID"

        document = {
            "registration_number": registration_number,
            "full_name": full_name,
            "unique_id": unique_id,
            "event_name": event_name,
            "email": email,
            "gender": gender,
            "role": role,
            "payment_status":payment_status
        }

        # result = collection.insert_one(document)

    except:
        print(f"{full_name}-{registration_number} already in database")

    try:
        print(f"{full_name}-{registration_number} QR succefully generated")

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(unique_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qrcode_dir = f"artifact/Event/{event_name}/QRCode/{registration_number}.png"
        img.save(qrcode_dir)
        print(f"QR Code {full_name}-{registration_number} saved here:- {qrcode_dir}")
    except:
        print(f"failed to generate QR for {full_name}-{registration_number}")





    pdf = PDF(event_img_filepath=f"artifact/Event/{event_name}/logo/logo.png")
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.heading(EVENT_NAME=event_name)
    pdf.date_time_venue(DATE_TIME_EVENT='28 February 2023, 4PM to 7PM', VENUE_EVENT='Where ever you find space')
    pdf.attendee_name(PER_NAME=full_name)
    pdf.role_in_event(ROLE=role)
    pdf.payment_status(PAYMENT=payment_status)
    pdf.order_number(order_no=unique_id)
    pdf.get_qr_code(qrcode_dir)

    pdf_dir = f"artifact/Event/{event_name}/TicketPDF/{registration_number}.pdf"
    pdf.output(pdf_dir, 'F')


# add new entries in database
# if qr not made then send entries of those to make qr
# if make pdf from those qr
# mail those tickcets to everyone
"""

Index(['payment button id', 'payment button title', 'payment date', 'order_id',
       'item name', 'item amount', 'item quantity', 'item payment amount',
       'total payment amount', 'currency', 'payment status', 'payment id',
       'email', 'phone', 'full_name', 'registration_number', 'gender'],
      dtype='object')

"""