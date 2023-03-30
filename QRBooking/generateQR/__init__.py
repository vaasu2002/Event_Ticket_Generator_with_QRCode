import pandas as pd
import qrcode
from QRBooking.constant import CONFIG_FILE_PATH
from QRBooking.common import read_yaml
from QRBooking.generateQR.mail import send_ticket
import os

configs = read_yaml(CONFIG_FILE_PATH)
payment_sheet_filepath = os.path.join(configs['artifact_dir'],configs['payment_sheet_dir'],'PUBJABI CLUB EVENT.xlsx')

from QRBooking.database import connectToDatabase
from QRBooking.generateQR.pdf import PDF
collection = connectToDatabase()

def make_qr(full_name:str,registration_number:str,unique_id:str,event_name:str):

    try:

        print(f"{registration_number}-{full_name} QR succefully generated")

        # Making QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(unique_id)
        qr.make(fit=True)

        # Saving QR in respective directory
        img = qr.make_image(fill_color="black", back_color="white")

        qrcode_dir = os.path.join(configs['artifact_dir'],"Event",configs['event_details']['event_name'],'QRCode',f"{registration_number}.png")

        img.save(qrcode_dir)

        print(f"{registration_number}-{full_name} QR Code saved here:- {qrcode_dir}")

        return qrcode_dir
    except:

        print(f"{registration_number}-{full_name} Failed to generate QR for ")


def generate_pdf(event_name:str,full_name:str,role:str,payment_status:str,
                    unique_id:str,qrcode_dir:str,registration_number:str,date_time_event=configs['event_details']['event_date_time'],venue_event=configs['event_details']['event_location']):
    
    try:

        event_img_filepath = os.path.join(configs['artifact_dir'],"Event",event_name,'logo','logo.png')
        pdf = PDF(event_img_filepath = event_img_filepath)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.heading(EVENT_NAME=event_name)
        pdf.date_time_venue(DATE_TIME_EVENT=date_time_event, VENUE_EVENT=venue_event)
        pdf.attendee_name(PER_NAME=full_name)
        pdf.role_in_event(ROLE=role)
        pdf.payment_status(PAYMENT=payment_status)
        pdf.order_number(order_no=unique_id)
        pdf.get_qr_code(qrcode_dir)

        pdf_dir = f"artifact/Event/{event_name}/TicketPDF/{registration_number}.pdf"

        pdf.output(pdf_dir, 'F')

        print(f"{registration_number}-{full_name} PDF saved here:- {pdf_dir}")

        return pdf_dir

    except Exception as e:
        print(e)


def start_entry_process():
    df = pd.read_excel(payment_sheet_filepath)
    confirm_payment_df = df[df['payment status']=='captured']
    failed_payment_df = df[df['payment status']=='failed']

    for index in range(0,len(confirm_payment_df)):
        # try:

        registration_number = confirm_payment_df['registration_number'].iloc[index].upper()
        unique_id = confirm_payment_df['order_id'].iloc[index]
        event_name = confirm_payment_df['payment button title'].iloc[index]
        email = confirm_payment_df['email'].iloc[index]
        full_name = confirm_payment_df['full_name'].iloc[index].upper()
        gender = confirm_payment_df['gender'].iloc[index].upper()
        role = "ATTENDEE"
        payment_status = "PAID"
        document = {
            "registration_number": registration_number,
            "full_name": full_name,
            "unique_id": unique_id,
            "event_name": event_name,
            "email": email,
            "gender": gender,
            "role": role,
            "payment_status":payment_status,
            "mailSent": False,
            "isInside": False,
        }
        try:
            result = collection.insert_one(document)
        
            

            qrcode_dir = make_qr(full_name,registration_number,unique_id,event_name)
            pdf_dir = generate_pdf(event_name,full_name,role,payment_status,
                        unique_id,qrcode_dir,registration_number)
                
            send_ticket(email,full_name,registration_number,event_name,pdf_dir)

        except:
            print(f"{registration_number}-{full_name} Already in database")

        


# add new entries in database
# if qr not made then send entries of those to make qr
# if make pdf from those qr
# mail those tickcets to everyone

# import pymongo

# # create a MongoClient instance
# client = pymongo.MongoClient("mongodb://localhost:27017/")

# # select a database and a collection
# db = client["mydatabase"]
# collection = db["mycollection"]

# # specify the query to find the document to update
# query = { "name": "John" }

# # specify the new feature to add to the document
# new_feature = { "$set": { "age": 30 } }

# # update the document with the new feature
# collection.update_one(query, new_feature)


# query = { "name": "John" }
# new_feature = { "$set": { "age": 30 } }
# collection.update_one(query, new_feature)