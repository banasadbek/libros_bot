import requests
import fitz 

BOT_TOKEN = '7763761681:AAEgbT3eRvvHUo_0a-YTcmZwg8LJNbNylzA'

CHANNEL_ID = '@libros_para_el'
import os

PDF_DIRECTORY = 'books'  

def send_photo_to_channel(bot_token, channel_id, photo_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    with open(photo_path, 'rb') as photo_file:
        files = {'photo': photo_file}
        data = {'chat_id': channel_id}
        response = requests.post(url, files=files, data=data)
    return response.json()

def send_document_reply(bot_token, channel_id, document_path, reply_to_message_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    with open(document_path, 'rb') as document_file:
        files = {'document': document_file}
        data = {
            'chat_id': channel_id,
            'reply_to_message_id': reply_to_message_id
        }
        response = requests.post(url, files=files, data=data)
    return response.json()

def extract_first_page_as_image(pdf_path, output_image_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    # Get the first page
    first_page = pdf_document[0]
    # Render the first page as a PNG image
    pix = first_page.get_pixmap()
    # Save the image to file
    pix.save(output_image_path)
    pdf_document.close()

# Loop through each PDF file in the directory
for filename in os.listdir(PDF_DIRECTORY):
    if filename.endswith('.pdf'):
        pdf_file_path = os.path.join(PDF_DIRECTORY, filename)
        cover_image_path = os.path.join(PDF_DIRECTORY, f'{os.path.splitext(filename)[0]}_cover.png')
        
        # Extract the first page of the PDF as an image
        extract_first_page_as_image(pdf_file_path, cover_image_path)
        
        # Send the cover image to the channel and capture the message ID
        send_photo_response = send_photo_to_channel(BOT_TOKEN, CHANNEL_ID, cover_image_path)
        message_id = send_photo_response.get("result", {}).get("message_id")
        
        if message_id:
            # Send the PDF file as a reply to the cover image
            send_document_response = send_document_reply(BOT_TOKEN, CHANNEL_ID, pdf_file_path, message_id)
            print(f"PDF Document Response for {filename}:", send_document_response)
        
        # Optional: delete cover image after sending to save space
        os.remove(cover_image_path)
