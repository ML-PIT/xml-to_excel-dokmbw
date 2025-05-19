import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from config import ABSENDER, EMPFÄNGER, EMAIL_PASSWORT, MAIL_BETREFF_VORLAGE, MAIL_TEXT, TESTMAIL_PW, SMTP1, ABSENDER_TEST

def sende_auswertung_per_mail(excel_dateien):
    datum = datetime.now().strftime("%d.%m.%Y")

    msg = EmailMessage()
    msg["Subject"] = MAIL_BETREFF_VORLAGE.format(datum)
    msg["From"] = ABSENDER
    msg["To"] = EMPFÄNGER
    msg.set_content(MAIL_TEXT)

    for datei in excel_dateien:
        with open(datei, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(datei)
            )

    with smtplib.SMTP(SMTP1, 587) as smtp:
        smtp.starttls()
        smtp.login(ABSENDER, EMAIL_PASSWORT)
        smtp.send_message(msg)
