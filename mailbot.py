import smtplib
from collections import defaultdict


class BioreactorGmailBot:
    def __init__(self, email, password):
        """ Initialises the bioreactor email bot
        The bot will first make sure that email is a valid Gmail account before logging onto Gmail with the valid email
        address and password.
        An empty stakeholder dictionary along with a tuple detailing the bot's email address and password
            will be created.

        Parameters
        ----------
        email (String): the email address of the bot (must be a Gmail address).
        password (String): password to the bot's Gmail account.
        """
        try:
            self.validate_gmail(email)
            self.sender_account_info = (email, password)
            self.stakeholders = defaultdict(lambda: "Value not found")
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            self.server.starttls()
            self.server.login(email, password)

        except NotGmailError:
            print(f"{email} is not a valid gmail email. Try again.")

    def send_message(self, to, subject, message):
        """ Sends a basic email to a particular email address

        Parameters
        ----------
        to (String): the email address of the person receiving this email.
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        """

        m = 'Subject: {}\n\n{}'.format(subject, message)
        self.server.sendmail(self.sender_account_info[0], to, m.encode('utf-8'))

    def send_to_all(self, subject="", message="", auto_heading=False):
        """ Sends an email all email addresses within self.stakeholders.

        Parameters
        ----------
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        auto_heading (Bool, optional): If True, message will be appended to "Hello {name},\n\n".
        """
        if auto_heading:
            def m(n):
                return f"Hello {n},\n\n" + message
        else:
            def m(n):
                return message
        for name, email in self.stakeholders.items():
            self.send_message(email, subject, m(name))

    def conditional_send(self, to, subject, message, condition, *args, auto_parse = False):
        """ Sends an email to a particular email address only if the condition is fulfilled.
        Also supports sending variable values via string parsing (look into auto_parse).

        Parameters
        ----------
        to (String): the email address of the person receiving this email.
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        condition (Bool || Function): A condition that needs to be fulfilled in order for the email to be sent.
        *args (List): Elements will be used by condition to check whether it has been fulfilled. Contents are
            also used to parse message.
        auto_parse (Bool, optional): If True, contents of *args will be used to parse {} of message.
        """
        message = self.parse_message(message, *args) if auto_parse else message
        if callable(condition):
            self.conditional_send(to, subject, message, condition(args))
        else:
            if condition:
                self.send_message(to, subject, message)

    def conditional_send_to_all(self, subject, message, condition, *args, auto_heading=False, auto_parse=False):
        """ Sends an email all email addresses within self.stakeholders only if the condition is fulfilled.
        Also supports sending variable values via string parsing (look into auto_parse).

        Parameters
        ----------
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        condition (Bool || Function): A condition that needs to be fulfilled in order for the email to be sent.
        *args (List): Elements will be used by condition to check whether it has been fulfilled. Contents are
            also used to parse message.
        auto_heading (Bool, optional): If True, message will be appended to "Hello {name},\n\n".
        auto_parse (Bool, optional): If True, contents of *args will be used to parse {} of message.
        """
        message = self.parse_message(message, *args) if auto_parse else message
        if callable(condition):
            self.conditional_send_to_all(subject, message, condition(args), auto_heading=auto_heading,
                                         auto_parse=auto_parse)
        else:
            if condition:
                self.send_to_all(subject, message, auto_heading)

    def add_stakeholder(self, name, email):
        self.stakeholders[name] = email

    def remove_stakeholder(self, name):
        self.stakeholders.pop(name)

    def clear_stakeholders(self):
        self.stakeholders.clear()

    def parse_message(self, message, *args):
        return message.format(*args)

    def validate_gmail(self, email):
        if email[-10:] != "@gmail.com":
            raise NotGmailError


class NotGmailError(Exception):
    pass


if __name__ == "__main__":
    application = BioreactorGmailBot("bioreactor.bot@gmail.com", "75q3@*NyiVDKmr_k")

    # application.send_message("jay.zhong@monashtechschool.vic.edu.au", "Test", "Testing, testing, one, two three...")
