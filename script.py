import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(filename='email_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

def send_email(subject, body, to_email, from_email, password, attachment_paths=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        if attachment_paths:
            for path in attachment_paths:
                attachment = open(path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(path)}')
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info('Email sent successfully to %s', to_email)
    except Exception as e:
        logging.error('Failed to send email', exc_info=True)

if __name__ == "__main__":
    from_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    # Define HTML content with basic page structure and CSS styling
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YOOOOH</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: pink;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Oya Boss!</h1>
            <p>This is a basic HTML email with CSS styling.</p>
        </div>
    </body>
    </html>
    """
    try:
        send_email(
            subject="Oya Boss, Tuendeleze Kazi!",
            body=html_content,
            to_email="nainawriters@gmail.com",
            from_email=from_email,
            password=password,
            attachment_paths=["g.pdf"]
        )
    except Exception as e:
        logging.error('Error running the script', exc_info=True)

