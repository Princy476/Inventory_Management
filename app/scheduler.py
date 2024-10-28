from apscheduler.schedulers.background import BackgroundScheduler
from app.email_notification import send_email_notification

def schedule_report():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email_notification, 'interval', days=1)
    scheduler.start()
