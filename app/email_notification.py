import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.database import get_items

def send_email_notification():
    items = get_items()
    low_stock_items = [item for item in items if item['quantity'] < item['threshold']]
    
    if low_stock_items:
        sender_email = "youremail@example.com"
        receiver_email = "receiver@example.com"
        password = "yourpassword"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Low Stock Alert"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        body = "The following items are low in stock:\n\n"
        for item in low_stock_items:
            body += f"Item: {item['item_name']}, Quantity: {item['quantity']}\n"
        
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
