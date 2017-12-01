from email.generator import Generator
from email.mime.text import MIMEText

from smtplib import SMTP

from user import user_exists


import os
import re


EMAIL_PATTERN = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def _format_sender(username):
    return '{}@reseauglo.ca'.format(username)


def _build_mail_obj(dest, subject, body, sender):
    mail = MIMEText(body)
    mail['From'] = sender
    mail['To'] = dest
    mail['Subject'] = subject
    return mail


def _save_mail(mail, username):
    if user_exists(username):
        mail_out_path = username

    else:
        err_dest_path = 'DESTERREUR'
        if not os.path.isdir(err_dest_path):
            os.mkdir(err_dest_path)

        mail_out_path = err_dest_path

    eml_file_path = os.path.join(mail_out_path, str(len(os.listdir(mail_out_path))) + '.eml')

    with open(eml_file_path, 'w') as out_eml_file:
        gen = Generator(out_eml_file)
        gen.flatten(mail)


def send_smtp(mail):
    conn = SMTP(host='smtp.ulaval.ca', timeout=10)

    conn.sendmail(mail['From'], mail['To'], mail.as_string())
    conn.quit()


def send_email(dest, subject, body, username):

    if not re.search(EMAIL_PATTERN, dest):
        raise ValueError('adresse "{}" invalide'.format(dest))

    mail = _build_mail_obj(dest, subject, body, _format_sender(username))

    if dest.endswith('@reseauglo.ca'):
        _save_mail(mail, dest.split('@')[0])

    else:
        send_smtp(mail)
