from smtplib import SMTP, SMTP_SSL
import ssl as pythonssllib

class SmtpTransport:

    def __init__(self, hostname, port=None, ssl=True, ssl_context=None, starttls=False):
        self.hostname = hostname

        if ssl:
            self.port = port or 465
            if ssl_context is None:
                ssl_context = pythonssllib.create_default_context()
            self.server = SMTP_SSL(self.hostname, self.port, context=ssl_context)
        else:
            self.port = port or 25
            self.server = SMTP(self.hostname, self.port)

        if starttls:
            self.server.starttls()

    def connect(self, username, password):
        self.server.login(username, password)
        return self.server