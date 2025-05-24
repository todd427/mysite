# myapp/email_backend.py
import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend

class UnsafeGmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        try:
            # Create the actual SMTP connection
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)

            # Bypass SSL verification
            context = ssl._create_unverified_context()
            self.connection.starttls(context=context)

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if not self.fail_silently:
                raise

