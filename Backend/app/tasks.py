from app import celery
from app.Models import Users, Ticket, Shows, Screening
from celery.schedules import crontab
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@celery.on_after_finalize.connect
def monthy_remainder_task(sender, **kwargs):
    sender.add_periodic_task(crontab(day_of_month=1), monthly_remainder.s())
    sender.add_periodic_task(crontab(hour="16", minute="30"), daily_remainder.s())

@celery.task()
def monthly_remainder():
    all_users = Users.query.all()
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    email_id = os.environ.get('email')
    password = os.environ.get('password')
    smtp.login(email_id, password)
    for user in all_users:
        tickets_booked = Ticket.query.filter_by(user_id = user.id)
        shows = []
        for ticket in tickets_booked:
            screening = Screening.query.filter_by(id = ticket.screening_id).first()
            show = Shows.query.filter_by(id = screening.show_id).first()
            show_date = datetime.strptime(screening.date, '%d/%m/%Y')
            now = datetime.now()
            dif = relativedelta(now, show_date)
            if(dif.months < 1):
                shows.append(show.name)
        try:
            m = MIMEMultipart()
            m['From'] = email_id
            m['To'] = user.email
            m['Subject'] = "Your monthly report!"
            shows_list_items = ''.join([f'<li>{show}</li>' for show in shows])
            email_content = f"<h1>Your dedicated and personalized monthly report is here!</h1><h3>These are the tickets you booked during the last month</h3><br><ol><b>{shows_list_items}</b></ol><br><br>Thanking you,<br>The TicketShow admins!"
            content = MIMEText(email_content, 'html')
            m.attach(content)
            smtp.sendmail(email_id, user.email, m.as_string())
        
        except Exception as e:
            print(e)

            

        

@celery.task()
def daily_remainder():
    all_users = Users.query.all()
    booked_tickets = [ticket.user_id for ticket in Ticket.query.with_entities(Ticket.user_id).all()]
    users_without_tickets = [user for user in all_users if user.id not in booked_tickets]
    email_id = os.environ.get('email')
    password = os.environ.get('password')
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(email_id, password)
        for user in users_without_tickets:
            try:
                m = MIMEMultipart()
                m['From'] = email_id
                m['To'] = user.email
                m['Subject'] = f"You are missing out"
                email_content = "<h1>The best offers are in town!</h1><br><br><h3>Visit TicketShow and book your first ticket today!</h3><br><br>Thanking You,<br>The TicketShow Admin!"
                content = MIMEText(email_content, 'html')
                m.attach(content)
                smtp.sendmail(email_id, user.email, m.as_string())
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    


