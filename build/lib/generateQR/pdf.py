from fpdf import FPDF
import pyqrcode
import png

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