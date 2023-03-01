EVENT_NAME = "EVENT NAME"
DATE_TIME_EVENT = "28 February 2023, 4PM to 7PM"
VENUE_EVENT = "Where ever you find space"
PER_NAME = "FULL NAME"
ROLE = "ATTENDEE"
PAYMENT_STATUS = "PAID"

from fpdf import FPDF
import pyqrcode
import png
from random import randint

ticket_order_number = []


def random_ticket_sequence():
    range_start = 10 ** (9 - 1)
    range_end = (10 ** 9) - 1
    ticket_order_number.append(randint(range_start, range_end))


random_ticket_sequence()

print(ticket_order_number)
index = 0
ORDER_NO = ticket_order_number[index]
# Generate QR code
url = pyqrcode.create(ORDER_NO)
url.png(f"{PER_NAME}_ticket.png", scale=6)


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
        self.set_x(-50)
        self.set_font("Arial", '', 10)
        # Order Number
        self.cell(0, 10, f"Order Number: {ORDER_NO}", 0, 0, 'L')

    def qr_code(self):
        # QR_CODE
        self.image(name=f"{PER_NAME}_ticket.png", x=170, y=85, w=25, h=25)

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
