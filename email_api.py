from fastapi import FastAPI
import uvicorn
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import email, smtplib, ssl
import base64
import json
import requests
from fastapi import Request

app = FastAPI()

@app.post("/email")
async def email(request: Request,order_number:str,user_email : str):
    data = await request.json()
    print(data)
    class EasyInvoice:

        @staticmethod
        def create(data):
            url = "https://api.easyinvoice.cloud/v2/free/invoices"
            data = {
                "data": data
            }
            response = requests.post(url, json=data)
            result = response.json()
            return result["data"]

        @staticmethod
        def save(invoice_base64, filename="invoice"):
            with open(filename + ".pdf", 'wb') as file:
                file.write(base64.b64decode(invoice_base64))
            with open(filename + ".png", 'wb') as file:
                file.write(base64.b64decode(invoice_base64))

            with open("imageT.png", "wb") as fh:
                fh.write(base64.urlsafe_b64decode(invoice_base64))

            # from PIL import Image
            # from base64 import decodestring
            #
            # image = Image.fromstring('RGB', (width, height), decodestring(imagestr))
            # image.save("foo.png")

    result = EasyInvoice.create(data)
    EasyInvoice.save(result["pdf"], order_number)
    sender_email = "order.5guyswholesale@gmail.com"
    receiver_email = "5guyswholesale@gmail.com"
    password = "kdmrszoxmvrpzjcg"
    subject = f"Order {order_number} confirmed"
    body = f"This is an confirm order of {user_email}"

    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # set the plain text body
    msg.set_content(body)

    with open('invoice.pdf', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='invoice123.pdf')

    text = msg.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


    return {"message": "Sucessfull"}

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8001, log_level="debug")