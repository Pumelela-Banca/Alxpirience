"""
Use this module to send emails using the MailerSend API.
"""
from mailersend import emails
from .data_base import User, Projects


key = open("expirience/access_token.txt", "r").read().rstrip("\n")

mailer = emails.NewEmail(key)

def send_to_job_taker(user_id: User.id, project_id: Projects.id):
    """
    sends email to user
    """
    mail_body = {}
    mail_from = {
    "name": "Axperience",
    "email": "pumelelaapps@gmail.com",
    }

    recipients = [
        {
            "email": User.query.get(user_id).email,
            "name": User.query.get(user_id).username
        }
    ]
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(f"Job Taken: {Projects.query.filter_by(id=project_id).first().project_name}",
                       mail_body)
    mailer.set_html_content(f"{Projects.query.filter_by(id=project_id).first().project_name}",
                            mail_body)
    mailer.set_plaintext_content(f"{Projects.query.filter_by(id=project_id).first().project_name}",
                                 mail_body)
    mailer.send(mail_body)


def send_to_job_poster(user_id: User.id, project_id: Projects.id):
    """
    sends email job poster 
    """
    mail_body = {}
    mail_from = {
    "name": "Axperience",
    "email": "pumelelaapps@gmail.com",
    }

    recipients = [
        {
            "email": Projects.query.filter_by(id=project_id).first().author.email,
            "name": Projects.query.filter_by(id=project_id).first().author.username,
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(f"Job Taken by {User.query.filter_by(id=user_id).first().username}",
                       mail_body)
    mailer.set_html_content(f"""I accept job that you posted at Alxpirience.
                            \nPlease send email  so we can sort out the details.\n
                            on {User.query.filter_by(id=user_id).first().email}""",
                            mail_body)
    mailer.set_plaintext_content(f"""I accept job that you posted at Alxpirience.
                            \nPlease send email  so we can sort out the details.\n
                            on {recipients[0]["email"]}""", mail_body)
    mailer.send(mail_body)
