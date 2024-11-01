import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.database import get_items
import requests
import json

def send_email_notification():
    items = get_items()
    low_stock_items = [
        {
            "item_name": item['item_name'],
            "available_quantity": item['quantity'],
            "low_quantity_threshold": item['threshold']
        }
        for item in items if item['quantity'] < item['threshold']
    ]
    
    if low_stock_items:
        # Define the JSON payload for the Logic App
        payload = {
            "subject": "Low Stock Alert",
            "items": low_stock_items
        }

        # Replace this URL with the HTTP POST URL of your Logic App
        logic_app_url = "https://prod-21.northcentralus.logic.azure.com:443/workflows/171a90d58cba404dac5b2f943e099c5c/triggers/When_a_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=HEBpFQZa0jK-pZBaTpsumdwNMtQshWhwL0kjAIxyM08"

        # Send a POST request to your Logic App
        response = requests.post(
            logic_app_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return "Email request sent successfully!"
        else:
            return f"Failed to send email request: {response.text}"
    else:
        return "No low stock items to notify."